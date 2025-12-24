import sys
import inspect
from utils import load_module

if __name__ == '__main__':

    if len(sys.argv) < 10:
        print(' '.join([
            "Usage: python3 exec.py",
            "[modin | pandas]",
            "<schema_path>",
            "<dataset_path> [csv | parquet] <external_path>",
            "<query_file>",
            "<scalar_udf_module> <aggr_udf_module> <table_udf_module>",
        ]))
        sys.exit(1)

    query_file_no_ext = sys.argv[6]
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

    pd_module_name = sys.argv[1]
    results = query_class(
        pd_module=pd_module_name,
        schema_module=load_module(sys.argv[2]),
        scalar_udf_path=sys.argv[7],
        aggr_udf_path=sys.argv[8],
        table_udf_path=sys.argv[9]
    ).exec(
        dataset_path=sys.argv[3],
        data_format=sys.argv[4],
        external_data_path=sys.argv[5]
    )
