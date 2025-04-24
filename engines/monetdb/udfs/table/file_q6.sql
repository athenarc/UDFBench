
-- U41.	File(q6): parses an external file (csv, xml, json) and returns a table 


CREATE or replace  FUNCTION file_q6(file_path2 STRING, file_type2 STRING)
RETURNS TABLE (column1 STRING, column2 STRING,column3 STRING, column4 STRING)
LANGUAGE PYTHON {

    import pandas as pd
    import xml.etree.ElementTree as ET
    import json
    import numpy as np

    def parse_csv(file_path):
        return pd.read_csv(file_path)

    def parse_xml(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        data = []
        columns = [child.tag for child in root[0]] if root else []

        for elem in root:
            row_data = [elem.find(column).text if elem.find(column) is not None else None for column in columns]
            data.append(row_data)

        return pd.DataFrame(data, columns=columns).fillna('')

            
    def parse_json(file_path):
        def iter_json(file_path):
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
  
        rows=[]
        for row in iter_json(file_path):
            rows.append(row)
        return pd.DataFrame(rows).fillna('')

    def parse_file(file_path, file_type):
        if file_type == 'csv':
            return parse_csv(file_path)
        elif file_type == 'xml':
            return parse_xml(file_path)
        elif file_type == 'json':
            return parse_json(file_path)
        else:
            raise ValueError("Unsupported file type")

    def file_parser_udf(file_path, file_type):
        table = parse_file(file_path, file_type)
        
        # Your additional processing or analysis using NumPy can go here
        table = table.astype(str)

        return table

    return file_parser_udf(file_path2, file_type2)
};
