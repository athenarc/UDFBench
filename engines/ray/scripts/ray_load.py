import os
import ray

def load_parquet_files(folder_path,map_schema):
    bench_datasets={}
    parquet_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".parquet"):
                parquet_files.append(os.path.join(root, file))



    if not parquet_files:
        print("No parquet files is this folder")
        return

    for file in parquet_files:
        table_name = os.path.basename(file).replace(".parquet", "")

        if table_name in map_schema:
            ds= ray.data.read_parquet(file
                )
            ds = ds.rename_columns(map_schema[table_name])
            # bench_datasets[table_name] = ds
            bench_datasets[table_name] = ds.materialize()
    return bench_datasets
