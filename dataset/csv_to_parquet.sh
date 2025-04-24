#!/bin/bash

CSV_IN_PATH=$1
PARQUET_OUT_PATH=$2
DATASET_NAME=$3
PYTHONEXEC=$4

$PYTHONEXEC <<EOF

import os
import pandas as pd

csv_in_path = "$CSV_IN_PATH"
parquet_out_path = "$PARQUET_OUT_PATH"
dataset_name = "$DATASET_NAME"


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
        
EOF
