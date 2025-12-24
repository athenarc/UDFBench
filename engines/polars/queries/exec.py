import sys
import inspect
from utils import load_module

if __name__ == '__main__':

    if len(sys.argv) < 9:
        print(' '.join([
            "Usage: python3 exec.py",
            "<schema_path>",
            "<dataset_path> [csv | parquet] <external_path>",
            "<query_file>",
            "<scalar_udf_module> <aggr_udf_module> <table_udf_module>",
        ]))
        sys.exit(1)

    query_file_no_ext = sys.argv[5]
    query_class = next((
        m[1] for m in inspect.getmembers(
            load_module(query_file_no_ext),
            inspect.isclass
        )
    ), None)
    if not query_class:
        print(
            f"Failed to find a query class in {query_file_no_ext}"
        )
        sys.exit(1)

    results = query_class(
        schema_module=load_module(sys.argv[1]),
        scalar_udf_path=sys.argv[6],
        aggr_udf_path=sys.argv[7],
        table_udf_path=sys.argv[8]
    ).exec(
        dataset_path=sys.argv[2],
        data_format=sys.argv[3],
        external_data_path=sys.argv[4]
    )
