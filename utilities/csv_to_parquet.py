import argparse
import os
import pandas as pd

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('csv_in_path')
arg_parser.add_argument('parquet_out_path')
arg_parser.add_argument('dataset_name')
args = arg_parser.parse_args()

csv_in_path = args.csv_in_path
parquet_out_path = args.parquet_out_path
dataset_name = args.dataset_name

for child in os.scandir(f'{csv_in_path}/{dataset_name}'):
    if child.is_file() and child.name.endswith('.csv'):
        out_dir = f'{parquet_out_path}/{dataset_name}/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        filename_no_ext = os.path.splitext(child.name)[0]
        path_table= f"{out_dir}{filename_no_ext}/"
        if not os.path.exists(path_table):
            os.makedirs(path_table)
        pd.read_csv(
            child.path,
            header=None
        ).to_parquet(
            f'{path_table}{filename_no_ext}.parquet')
        