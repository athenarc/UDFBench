
from udfs.aggregate.aggregate_avg import Aggregate_avg
from udfs.scalar import jsoncount
import pyarrow as pa

def run_query(datasets,folder_path=None):
    artifact_citations = datasets["artifact_citations"]

    artifact_authorlists = datasets["artifact_authorlists"]



    results = ( 
        artifact_citations.join(
        artifact_authorlists,
        on=("artifactid",),
        join_type="inner",
        num_partitions = 4)
        .map_batches(lambda batch: pa.table({
            "target_count":  jsoncount(batch["target"]),
            "authorlist_count":  jsoncount(batch["authorlist"]),
        }), batch_format="pyarrow")
        .groupby(None)
        .aggregate(
            Aggregate_avg("target_count"),
            Aggregate_avg("authorlist_count")
        )
    )
    return results