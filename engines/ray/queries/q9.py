import ray
from ray.data.expressions import col
from udfs.aggregate.aggregate_count import Aggregate_count
from udfs.scalar import jsoncount,clean
from udfs.table import combinations
import pyarrow as pa


def run_query(datasets,folder_path=None):
    artifact_authorlists = datasets["artifact_authorlists"]
    results = (artifact_authorlists.map_batches(lambda batch: pa.table({
            "artifactid": batch["artifactid"],
            "authorlist":  batch["authorlist"],
            "jsoncount":  jsoncount(batch["authorlist"]),
        }), batch_format="pyarrow")
        .filter(expr=col("jsoncount") <= 50)
        .map_batches(lambda batch: pa.table({
            "artifactid": batch["artifactid"],
            "authorlist":  clean(batch["authorlist"]),
        }), batch_format="pyarrow")
        .map_batches(
            combinations,
            batch_format="pyarrow",
            fn_kwargs={"N": 2}
        )
        .groupby(None).aggregate(Aggregate_count())

    )
    return results
