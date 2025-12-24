from udfs.aggregate.aggregate_avg import Aggregate_avg
from udfs.aggregate.aggregate_median import Aggregate_median

def run_query(datasets,folder_path=None):
    artifacts = datasets["artifacts"]
    author_col = artifacts.select_columns(["authors"])
    results = author_col.groupby(None).aggregate(Aggregate_avg("authors"),Aggregate_median("authors"))
    return results