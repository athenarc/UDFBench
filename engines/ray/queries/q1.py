from udfs.scalar import extractyear, extractmonth, extractday
import pyarrow as pa

def run_query(datasets,folder_path=None):
    artifacts = datasets["artifacts"]
    results = artifacts.select_columns(["id","date"]).map_batches(lambda batch: pa.table({
    "id": batch["id"],
    "year":  extractyear(batch["date"]),
    "month": extractmonth(batch["date"]),
    "day": extractday(batch["date"])
}), batch_format="pyarrow")
    return results
