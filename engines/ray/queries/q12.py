
from udfs.scalar import cleandate, addnoise
from ray.data.aggregate import Count
from datetime import datetime, timedelta
import pyarrow as pa
import pyarrow.compute as pc

def run_query(datasets,folder_path=None):
    views_stats = datasets["views_stats"]

    views_stats_sel = views_stats.map_batches(lambda batch: pa.table({
    "artifactid": batch["artifactid"],
    "cleandate":  cleandate(batch["date"]),
}), batch_format="pyarrow")

   
    filtered = views_stats_sel.map_batches(
        lambda batch: batch.filter(
            pc.greater_equal(
                pc.strptime(batch["cleandate"], format="%Y/%m/%d", unit="us"),
                pa.scalar( datetime.now() - timedelta(days=32*30), pa.timestamp("us"))
            )
        ),
        batch_format="pyarrow"
    )

    results = filtered.groupby("artifactid").aggregate(Count())\
    .map_batches(
        lambda batch: pa.table({
    "artifactid": batch["artifactid"],
    "views":  addnoise(batch["count()"]),
}), batch_format="pyarrow"
    )
    results = results.sort("views", descending=True).limit(10)
    return results
