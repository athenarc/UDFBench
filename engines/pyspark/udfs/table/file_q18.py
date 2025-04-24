import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

# U41.	File: parses an external file (csv, xml, json) and returns a table 
def file(file_path: str, file_type:str):    
    import csv
    import os
    import json
    import xml.etree.ElementTree as ET
    import pandas as pd

    def parse_csv(file_path):
        df = pd.read_csv(file_path,header=None)
        df = df.where(pd.notnull(df), None)
        for _, row in df.iterrows():
                yield tuple(row.values)


    def parse_csv2(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield tuple(row.values())

    def read_json(file_path):
        with open(file_path, 'r') as file:
            first_character = file.read(1)
            file.seek(0)  # Reset the file pointer to the beginning
            if first_character == '[':
                data = json.load(file)
                if isinstance(data, list):
                    for item in data:
                        yield tuple(item.values())
                elif isinstance(data, dict):
                    yield tuple(data.values())
            else:
                for line in file:
                    data = json.loads(line)
                    if isinstance(data, list):
                        for item in data:
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        yield tuple(data.values())

    def read_xml(file_path):
        def parse_xml(xml_file_path):
            root = ET.parse(xml_file_path).getroot()
            data = []
            columns = []
            
            for elem in root:
                if not columns:
                    columns = [child.tag for child in elem]

                row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
                data.append(row_data)
            return data
        for record in parse_xml(file_path):
            yield tuple(record)

    def parse_text(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            for _line in lines:
                yield (_line,)

    if file_type == 'csv':
        return parse_csv(file_path)
    elif file_type == 'json':
        return read_json(file_path)
    elif file_type == 'xml':
        return read_xml(file_path)
    elif file_type == 'text':
        return parse_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_type}")
        return None



@udtf(returnType="column1 STRING, column2 STRING")
class File_q18:
    def eval(self, file_path: str, file_type:str):
        return file(f"{file_path}",file_type)
 