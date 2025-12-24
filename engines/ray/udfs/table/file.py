import csv
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd
import pyarrow as pa

# U41.	File: parses an external file (csv, xml, json) and returns a table 




def parse_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.where(pd.notnull(df), None)  
    table = pa.Table.from_pandas(df)
    return table

def parse_json(file_path):
    rows=[]
    with open(file_path, 'r') as file:
        first_character = file.read(1)
        file.seek(0)
        if first_character == '[':
            data = json.load(file)
            if isinstance(data, list):
                for item in data:
                    rows.append(item)
            elif isinstance(data, dict):
                rows.append(data)

        else:
            for line in file:
                data = json.loads(line)
                rows.append(data)
    return pa.Table.from_pylist(rows)

def parse_text(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        return pa.table({
        "line": pa.array(lines, pa.string()),
  })

def file(batch, file_path=None, file_type=None):
    if file_type == "csv":
        return parse_csv(file_path)
    elif file_type == "json":
        return parse_json(file_path)
    elif file_type == "text":
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
