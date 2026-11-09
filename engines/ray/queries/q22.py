def run_query(datasets, folder_path=None):
    import pandas as pd
    import pyarrow as pa

    from udfs.scalar.dlpredict_citations import dlpredict_citations
    from udfs.scalar.extractfunder import extractfunder
    from udfs.scalar.extractyear import extractyear

    NUM_PARTITIONS = 8

    # ==================================================================
    # RENAME POSITIONAL PARQUET COLUMNS TO SQL SCHEMA NAMES
    #
    # The Parquet files contain columns named 0, 1, 2, ...
    # The original UDFBench SQL schema defines their semantic names.
    # ==================================================================

    datasets["artifacts"] = datasets["artifacts"].rename_columns({
        "0": "id",
        "1": "title",
        "2": "publisher",
        "3": "journal",
        "4": "date",
        "5": "year",
        "6": "access_mode",
        "7": "embargo_end_date",
        "8": "delayed",
        "9": "authors",
    })

    datasets["artifact_authors"] = datasets["artifact_authors"].rename_columns({
        "0": "artifactid",
        "1": "affiliation",
        "2": "fullname",
        "3": "name",
        "4": "surname",
        "5": "rank",
        "6": "authorid",
    })

    datasets["projects_artifacts"] = datasets["projects_artifacts"].rename_columns({
        "0": "projectid",
        "1": "artifactid",
        "2": "provenance",
    })

    datasets["projects"] = datasets["projects"].rename_columns({
        "0": "id",
        "1": "acronym",
        "2": "title",
        "3": "funder",
        "4": "fundingstring",
        "5": "funding_lvl0",
        "6": "funding_lvl1",
        "7": "funding_lvl2",
        "8": "ec39",
        "9": "type",
    })

    datasets["artifact_citations"] = datasets["artifact_citations"].rename_columns({
        "0": "artifactid",
        "1": "target",
        "2": "citcount",
    })

    # ==================================================================
    # READ INPUT DATA
    # ==================================================================

    a = datasets["artifacts"].select_columns([
        "id",
        "title",
        "date",
    ])

    au = datasets["artifact_authors"].select_columns([
        "artifactid",
        "authorid",
    ])

    project_links = datasets["projects_artifacts"].select_columns([
        "artifactid",
        "projectid",
    ])

    p = datasets["projects"].select_columns([
        "id",
        "fundingstring",
    ])

    ac = datasets["artifact_citations"].select_columns([
        "artifactid",
        "citcount",
    ])

    # ==================================================================
    # RENAME JOIN KEYS
    # ==================================================================

    au = au.rename_columns({
        "artifactid": "id",
    })

    project_links = project_links.rename_columns({
        "artifactid": "id",
        "projectid": "project_id",
    })

    p = p.rename_columns({
        "id": "project_id",
    })

    ac = ac.rename_columns({
        "artifactid": "id",
    })

    # ... rest of your existing Q25 ...



    def count_authors(group):
        return pd.DataFrame({
            "id": [group["id"].iloc[0]],
            "author_count": [group["authorid"].nunique()],
        })

    author_counts = (
        au
        .groupby("id")
        .map_groups(
            count_authors,
            batch_format="pandas",
        )
    )

    # ==================================================================
    # EXTRACT FUNDER AND FILTER FP7
    #
    # Pandas equivalent:
    #
    # p['funder'] = p['fundingstring'].apply(extractfunder)
    # p = p[p['funder'] == 'FP7']
    #
    # We deliberately do this before joining projects to artifacts.
    #
    # The filtering happens INSIDE map_batches rather than:
    #
    #     p.filter(fn=...)
    #
    # so we avoid:
    #
    # "Use 'expr' instead of 'fn' when possible for performant filters."
    # ==================================================================

    def extract_funder_and_filter(batch):
        batch = batch.copy()

        batch["funder"] = extractfunder(
            pa.array(batch["fundingstring"])
        )

        return batch[
            batch["funder"] == "FP7"
        ][
            ["project_id"]
        ]

    p = p.map_batches(
        extract_funder_and_filter,
        batch_format="pandas",
        batch_size=200,
        num_gpus=1,
    )

    # ==================================================================
    # PROJECT FILTER
    #
    # Original:
    #
    # pa.merge(p)
    #
    # Since p now contains only FP7 projects, this establishes the
    # exact same membership condition.
    #
    # We can safely remove duplicate artifact/project links here because
    # the original query eventually does:
    #
    #     drop_duplicates('id')
    #
    # and projectid is not part of the final output or prediction.
    # ==================================================================

    project_links = project_links.join(
        p,
        on=["project_id"],
        num_partitions=NUM_PARTITIONS,
        join_type="inner",
    )

    def keep_one_project_artifact(group):
        return group.iloc[[0]][["id"]]

    project_links = (
        project_links
        .groupby("id")
        .map_groups(
            keep_one_project_artifact,
            batch_format="pandas",
        )
    )

    # At this point:
    #
    # project_links = one row per artifact having an FP7 project.
    #
    # This is equivalent to the existence condition imposed by:
    #
    # a.merge(pa).merge(p).drop_duplicates('id')

    # ==================================================================
    # MAIN JOINS
    #
    # We deliberately DO NOT deduplicate here.
    #
    # The original Pandas query performs:
    #
    #     a
    #     .merge(ab)
    #     .merge(counts)
    #     .merge(pa)
    #     .merge(p)
    #     .merge(ac, how='left')
    #     .drop_duplicates('id')
    #
    # Therefore we preserve all possible duplicate rows until the
    # equivalent final operation below.
    # ==================================================================

    fofo = a.join(
        author_counts,
        on=["id"],
        num_partitions=NUM_PARTITIONS,
        join_type="inner",
    )

    fofo = fofo.join(
        project_links,
        on=["id"],
        num_partitions=NUM_PARTITIONS,
        join_type="inner",
    )

    fofo = fofo.join(
        ac,
        on=["id"],
        num_partitions=NUM_PARTITIONS,
        join_type="left_outer",
    )

    # ==================================================================
    # EXACT EQUIVALENT OF:
    #
    #     .drop_duplicates('id')
    #
    # IMPORTANT:
    # This is deliberately done AFTER the citation left join.
    # ==================================================================

    def drop_duplicates_id(group):
        return group.iloc[[0]]

    fofo = (
        fofo
        .groupby("id")
        .map_groups(
            drop_duplicates_id,
            batch_format="pandas",
        )
    )

    # ==================================================================
    # EXTRACT YEAR
    #
    # Pandas:
    #
    # a['year'] = a['date'].apply(extractyear)
    #
    # ==================================================================

    def apply_extractyear(batch):
        batch = batch.copy()

        batch["year"] = extractyear(
            pa.array(batch["date"])
        )

        return batch

    fofo = fofo.map_batches(
        apply_extractyear,
        batch_format="pandas",
    )

    # ==================================================================
    # PREDICT IMPACT
    #
    # Pandas equivalent:
    #
    # fofo['predicted_impact'] = fofo.apply(
    #     lambda r: dlpredict_citations(...),
    #     axis=1
    # )
    #
    # We retain row-wise invocation because this preserves the semantics
    # of the scalar UDF.
    # ==================================================================

    def apply_dlpredict(batch):
        batch = batch.copy()

        predictions = []

        for row in batch.itertuples(index=False):
            # Pandas:
            #
            # r['citcount'] if pd.notna(r['citcount']) else 0
            #
            current_citations = (
                0
                if pd.isna(row.citcount)
                else row.citcount
            )

            predictions.append(
                dlpredict_citations(
                    row.author_count,
                    current_citations,
                    row.year,
                    "cuda",
                )[0]
            )

        batch["predicted_impact"] = predictions

        return batch

    fofo = fofo.map_batches(
        apply_dlpredict,
        batch_format="pandas",
        num_gpus=1,
        batch_size = 200
    )

    # ==================================================================
    # ORDER BY predicted_impact DESC
    # LIMIT 20
    #
    # Equivalent to:
    #
    # fofo.sort_values(
    #     'predicted_impact',
    #     ascending=False
    # ).head(20)
    # ==================================================================

    result = (
        fofo
        .sort(
            "predicted_impact",
            descending=True,
        )
        .limit(20)
        .select_columns([
            "id",
            "title",
            "predicted_impact",
            "citcount",
        ])
    )

    result.show()

    return result
