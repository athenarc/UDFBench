import duckdb
import os
import pandas as pd
import numpy as np

# U41.	File: parses an external file (csv, xml, json) and returns a table 

def file(self,file_path:str,file_type:str):
    import pandas as pd
    import xml.etree.ElementTree as ET
    import numpy as np
    import json
    import os

    def parse_csv(file_path):
        return pd.read_csv(file_path,header=None)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = []

        for elem in root:
            if not columns:
                columns = [child.tag for child in elem]

            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns).fillna('')

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

        return pd.DataFrame(rows)

    def parse_text(file_path):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
            return pd.DataFrame(lines,columns=['line'])

    def parse_file_TYPE(file_path, file_type):
        if file_type == 'csv':
            res= parse_csv(file_path)
            if 0 in res.columns:
                res.columns = [f"column{i}" for i in range(res.shape[1])]
            return res
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        elif file_type == 'text':
            return parse_text(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file_TYPE(file_path, file_type)
        # table = table.astype(str)
        table = table.where(pd.notnull(table), None)

        return table

    res = file_parser_udf(str(self.external_path)+'/'+str(file_path[0]), str(file_type[0]))  
    # records = [{col: row[col] for col in ['doi', 'amount', 'totalpubs','sdate']} for index, row in res.iterrows()]
    return [res.to_dict('records')]
