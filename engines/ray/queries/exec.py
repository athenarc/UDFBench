import sys
import importlib
import ray
import psutil, os, time
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def get_cpu_time_in_ms():
    parent = psutil.Process(os.getpid())
    total = 0.0
    try:
        pt= parent.cpu_times()
        total = pt.user + pt.system
        for child in parent.children(recursive=True):
            try:
                ct = child.cpu_times()
                total += ct.user + ct.system
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    return total * 1000.0

def load_query(query_name):
    module = importlib.import_module(f"queries.q{query_name}")
    if not hasattr(module, "run_query"):
        raise ValueError("Query must define run_query(datasets,file_path)")
    return module.run_query

if __name__ == "__main__":
    import os
    import argparse

    import sys
    import time
    import psutil
    
    from ray._private.ray_logging.logging_config import LoggingConfig
    from ray.data.context import DataContext
    import logging
    
    parser = argparse.ArgumentParser(description='Run Ray UDF benchmarks')
    parser.add_argument('--print-stats', help='Enable stats', action='store_true')
    parser.add_argument('--nthreads', help='Number of threads')
    parser.add_argument('--temp-dir', help='Path to the Ray temp directory')
    parser.add_argument('--ray-parquet', help='Path to the Ray parquet files')
    parser.add_argument('--ray-external', help='Path to the external files')
    parser.add_argument('--ray-query', help='The number of the query')
    parser.add_argument('--print-results', help='Print the query results', action='store_true')


    args = parser.parse_args()
    run_ray = False
    print_results = False
    stats = False
    external_path = None
    database_path = None
    temp_dir = None
    nthreads = None

    if args.ray_query:
        query_name = str(args.ray_query)
        if args.ray_parquet:
            if os.path.exists(args.ray_parquet):
                database_path = str(args.ray_parquet)
            else:
                print("Parquet directory does not exist")
                sys.exit(2)
        if args.ray_external:
            if os.path.exists(args.ray_external):
                external_path = str(args.ray_external)
            else:
                print("External directory does not exist")
                sys.exit(2)
        if args.temp_dir:
            if os.path.exists(args.temp_dir):
                temp_dir = str(args.temp_dir)
            else:
                print("Temporary directory does not exist")
                sys.exit(2)
        if args.nthreads:
            try:
                nthreads = int(args.nthreads)
            except:
                print("Wrong arguments. Please provide a valid integer value for nthreads.")
    else:
        print("Query number required")
        sys.exit(2)

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )

    sys.path.insert(0,project_root)
    NUMCPUS = nthreads
    TEMP_DIR = temp_dir
    WORKING_DIR = project_root
    FILE_PATH = external_path

    logging.basicConfig(level=logging.ERROR)
    logging.getLogger("ray").setLevel(logging.ERROR)
    logging.getLogger("ray.data").setLevel(logging.ERROR)
    ray.init(
        runtime_env={"working_dir": WORKING_DIR}, 
        log_to_driver=False,
        _temp_dir= TEMP_DIR,
        num_cpus = NUMCPUS,
        logging_config=LoggingConfig(log_level=logging.ERROR)
    )
    DataContext.get_current().enable_progress_bars = False

    from scripts.ray_schema import udfbench_schema
    from scripts.ray_load import load_parquet_files
    datasets = load_parquet_files(database_path,udfbench_schema)
    run_query = load_query(query_name)
    start_cpu = get_cpu_time_in_ms()
    start = time.time()

    result_ds = run_query(datasets,FILE_PATH)
    if result_ds:
        result_ds.materialize()

    end = time.time()
    end_cpu = get_cpu_time_in_ms()


    print(f'Execution Time: {(end-start)*1000:.3f} ms\n')
    print(f'Process Time: {(end_cpu-start_cpu):.3f} ms\n')

    if args.print_results:
        if result_ds:
            result_ds.show()

    if args.print_stats:
        if result_ds:
            result_ds.stats()

    ray.shutdown()
    sys.exit(0)