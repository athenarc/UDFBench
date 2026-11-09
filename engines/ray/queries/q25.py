import ray
import pyarrow as pa
from ray.data.expressions import col


def run_query(datasets, folder_path=None):
    from udfs.scalar.extractfunder import extractfunder
    from udfs.scalar.extractyear import extractyear
    from udfs.aggregate.dl_embed_agg import dl_embed_agg

    datasets["artifacts"] = datasets["artifacts"].rename_columns({
        "0": "artifactid",
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

    datasets["projects_artifacts"] = datasets["projects_artifacts"].rename_columns({
        "0": "projectid",
        "1": "artifactid",
        "2": "provenance",
    })

    datasets["projects"] = datasets["projects"].rename_columns({
        "0": "projectid",
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

    # ---------------------------------------------------------
    # Projects
    # Keep only the columns needed for the query.
    # This also avoids the duplicate "funder" column.
    # ---------------------------------------------------------
    projects = (
        datasets['projects']
        .select_columns(['projectid', 'fundingstring'])
        .map_batches(
            lambda b: b.append_column(
                'funder',
                extractfunder(b['fundingstring'])
            ),
            batch_format='pyarrow'
        )
    )

    # ---------------------------------------------------------
    # Artifacts
    # Extract year and push the year filter before the joins.
    # ---------------------------------------------------------
    artifacts = (
        datasets['artifacts']
        .select_columns(['artifactid', 'date'])
        .map_batches(
            lambda b: b.append_column(
                'year',
                extractyear(b['date'])
            ),
            batch_format='pyarrow'
        )
        .filter(expr=col('year') > 2020)
        .select_columns(['artifactid'])
    )

    # ---------------------------------------------------------
    # Projects -> Projects/Artifacts -> Artifacts
    # ---------------------------------------------------------
    rows = (
        projects
        .join(
            datasets['projects_artifacts'],
            on=['projectid'],
            join_type='inner',
            num_partitions=8
        )
        .join(
            artifacts,
            on=['artifactid'],
            join_type='inner',
            num_partitions=8
        )
    )

    # ---------------------------------------------------------
    # Join abstracts and remove NULL abstracts
    # ---------------------------------------------------------
    rows = (
        rows
        .join(
            datasets['artifact_abstracts'],
            on=['artifactid'],
            join_type='inner',
            num_partitions=8
        )
        .filter(expr=col('abstract').is_not_null())
    )

    # ---------------------------------------------------------
    # Only the columns needed by the Python aggregation
    # ---------------------------------------------------------
    frame = (
        rows
        .select_columns(['funder', 'abstract'])
        .to_pandas()
    )

    # ---------------------------------------------------------
    # Group by funder and compute the embedding aggregate
    # ---------------------------------------------------------
    result = (
        frame
        .groupby('funder', dropna=False)['abstract']
        .apply(
            lambda texts: dl_embed_agg(
                texts,
                'sentence-transformers/all-MiniLM-L6-v2',
                'cuda'
            )
        )
        .reset_index(name='funder_embedding')
    )

    return ray.data.from_pandas(result)
