from udfs.table import extractfromdate
import pyarrow as pa

def run_query(datasets,folder_path=None):
    artifacts = datasets["artifacts"]
    return artifacts.select_columns(["id","date"]).map_batches(
    extractfromdate,
    batch_format="pyarrow"
)