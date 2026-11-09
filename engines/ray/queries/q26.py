import ray
import pyarrow as pa
from ray.data.expressions import col


def run_query(datasets, folder_path=None):
    from udfs.scalar.blockkey import blockkey
    from udfs.scalar.extractyear import extractyear
    from udfs.scalar.jsoncount import jsoncount
    from udfs.scalar.keywords import keywords
    from udfs.scalar.filterstopwords import filterstopwords
    from udfs.scalar.stem import stem
    from udfs.scalar.frequentterms import frequentterms
    from udfs.table.resolveauthors import resolveauthors

    # ============================================================
    # RENAME POSITIONAL PARQUET COLUMNS TO SQL SCHEMA NAMES
    #
    # Parquet files contain columns 0, 1, 2, ...
    # ============================================================

    datasets["artifact_authors"] = datasets["artifact_authors"].rename_columns({
        "0": "artifactid",
        "1": "affiliation",
        "2": "fullname",
        "3": "name",
        "4": "surname",
        "5": "rank",
        "6": "authorid",
    })

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

    datasets["artifact_abstracts"] = datasets["artifact_abstracts"].rename_columns({
        "0": "artifactid",
        "1": "abstract",
    })

    datasets["artifact_authorlists"] = datasets["artifact_authorlists"].rename_columns({
        "0": "artifactid",
        "1": "authorlist",
    })

    # ------------------------------------------------------------
    # artifact_authors
    # WHERE au.rank = 1
    # ------------------------------------------------------------

    authors = datasets["artifact_authors"].filter(
        expr=col("rank") == 1
    ).select_columns([
        "artifactid",
        "fullname",
        "affiliation",
    ])

    # ------------------------------------------------------------
    # blockkey(au.fullname, au.affiliation)
    # ------------------------------------------------------------

    authors = authors.map_batches(
        lambda batch: batch.append_column(
            "bkey",
            blockkey(
                batch["fullname"],
                batch["affiliation"]
            )
        ),
        batch_format="pyarrow"
    )

    # ------------------------------------------------------------
    # JOIN artifacts
    # ------------------------------------------------------------

    rows = authors.join(
        datasets["artifacts"]
            .rename_columns({"id": "artifactid"})
            .select_columns([
                "artifactid",
                "date",
            ]),
        join_type="inner",
        on=["artifactid"],
        num_partitions=4
    )

    # ------------------------------------------------------------
    # extractyear(a.date) = 2010
    # ------------------------------------------------------------

    rows = rows.map_batches(
        lambda batch: batch.append_column(
            "event_year",
            extractyear(batch["date"])
        ),
        batch_format="pyarrow"
    ).filter(
        expr=col("event_year") == 2010
    )

    # ------------------------------------------------------------
    # JOIN artifact_abstracts
    # ------------------------------------------------------------

    rows = rows.join(
        datasets["artifact_abstracts"].select_columns([
            "artifactid",
            "abstract",
        ]),
        join_type="inner",
        on=["artifactid"],
        num_partitions=4
    )

    # ------------------------------------------------------------
    # LEFT JOIN artifact_authorlists
    # ------------------------------------------------------------

    rows = rows.join(
        datasets["artifact_authorlists"].select_columns([
            "artifactid",
            "authorlist",
        ]),
        join_type="left_outer",
        on=["artifactid"],
        num_partitions=4
    )

    # ------------------------------------------------------------
    # COALESCE(authorlist, '[]')
    # ------------------------------------------------------------

    rows = rows.map_batches(
        lambda batch: batch.set_column(
            batch.schema.get_field_index("authorlist"),
            "authorlist",
            pa.array([
                "[]" if value is None else value.as_py()
                for value in batch["authorlist"]
            ])
        ),
        batch_format="pyarrow"
    )

    # ------------------------------------------------------------
    # jsoncount(COALESCE(authorlist, '[]')) < 5
    # ------------------------------------------------------------

    rows = rows.map_batches(
        lambda batch: batch.append_column(
            "coauthor_count",
            jsoncount(batch["authorlist"])
        ),
        batch_format="pyarrow"
    ).filter(
        expr=col("coauthor_count") < 5
    )

    # ------------------------------------------------------------
    # topic_terms
    # ------------------------------------------------------------

    rows = rows.map_batches(
        lambda batch: batch.append_column(
            "topic_terms",
            frequentterms(
                stem(
                    filterstopwords(
                        keywords(batch["abstract"])
                    )
                ),
                10
            )
        ),
        batch_format="pyarrow"
    )

    # ------------------------------------------------------------
    # Exact input schema for resolveauthors
    # ------------------------------------------------------------

    rows = rows.map_batches(
        lambda batch: pa.table({
            "artifact_id": batch["artifactid"],
            "bkey": batch["bkey"],
            "raw_name": batch["fullname"],
            "raw_affil": batch["affiliation"],
            "coauthors": batch["authorlist"],
            "topic_terms": batch["topic_terms"],
            "event_date": batch["date"],
        }),
        batch_format="pyarrow"
    )

    # ------------------------------------------------------------
    # resolveauthors(...)
    # ------------------------------------------------------------

    return rows.map_batches(
        lambda batch: resolveauthors(
            batch,
            "sentence-transformers/all-MiniLM-L6-v2",
            "cuda"
        ),
        batch_format="pyarrow",
        batch_size=200,
        num_gpus=1,
        
    )



