import ray
import sys
from udfs.aggregate.aggregate_avg import Aggregate_avg
from udfs.scalar import jsoncount
from udfs.table import file
import pyarrow as pa

def run_query(datasets,folder_path=None):
    if folder_path:
        ds =ray.data.from_items([1])
        ds_file = ds.map_batches(
            file,
            batch_format="pyarrow",
            fn_kwargs={"file_path": f"{folder_path}/pubmed_q7.txt", "file_type": "json"}
        )
        results = ( 
            ds_file.map_batches(lambda batch: pa.table({
                "citations_count":  jsoncount(batch["citations"]),
                "authors_count":  jsoncount(batch["authors"]),
            }), batch_format="pyarrow")
            .groupby(None)
            .aggregate(
                Aggregate_avg("citations_count"),
                Aggregate_avg("authors_count")
            )
        )
        return results
    else:
        print("Error, --ray-query, --ray-external need to be specified together", file=sys.stderr)
        sys.exit(2)
