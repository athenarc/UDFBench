import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

    
# U30.	Extractfromdate(v2): Reads a date (as a string) and returns 3 column values (year, month, day)

@udtf(returnType="id string,year int, month int, day int")
class ExtractFromDate:
    def eval(self, args: list):
            (id,arg) = args
            if arg:
                try:
                    yield (id,int(arg[:arg.find('-')]), \
                            int(arg[arg.find('-')+1:arg.rfind('-')]), \
                            int(arg[arg.rfind('-')+1:]))
                    
                except:
                    yield(id, -1,-1,-1)
            else: yield(id,None,None,None)



#  U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values

@udtf(returnType="publicationdoi string, fundinginfo string")
class JsonParse:
    def eval(self, json_content: list, key1: str, key2: str):
        for json_str in json_content:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict):
                    yield (data.get(key1), data.get(key2))
                else:
                    yield (None, None)
            except:
                yield (None, None)



# U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

@udtf(returnType="authorpairs: string")
class Combinations:
    def eval(self, vals: str, N:int):
        # for val in vals:
            if vals:
                try:
                    name_list = json.loads(vals[0])
                    for name_per in itertools.combinations(name_list, N):
                        yield (json.dumps(list(name_per)),)
                except:
                    yield ('[]')
            else:
                yield None 

# U32.	Combinations(v2 for q16): Reads a json list and returns a table with all the combinations per an integer parameter


@udtf(returnType="pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string,authorpair string")
class Combinations_q16:
    import json
    import itertools
    from itertools import combinations

    def eval(self, vals: Row, N:int):
        if vals:
            if len(vals) == 8:
                try:
                    name_list = json.loads(vals[7])
                    for name_per in itertools.combinations(name_list, N):
                        yield (vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],json.dumps(list(name_per)),)
                except:
                    yield (vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],'[]')
            else:
                yield  (None,None,None,None,None,None,None,None)
        else:
            yield  (None,None,None,None,None,None,None,None)




#  U33.	Extractkeys: Selects keys from xml parsed input 

@udtf(returnType="publicationdoi string, fundinginfo string")
class Extractkeys:
    def eval(self,jvals:list,key1:str,key2:str):
        for jval in jvals:
            try:
                data = json.loads(jval)
                if isinstance(data, list):
                    for item in data:
                        yield  (item.get(key1), item.get(key2))
                elif isinstance(data, dict):
                    yield  (data.get(key1),data.get(key2))
                else:
                    yield (None,None)
            except:
                yield (None,None)





#  U38.	Xmlparser :  Parses xml input and returns a table 


@udtf(returnType="record string")
class Xmlparser:
    def eval(self, xml_content: list, root_name: str):
        import xml.etree.ElementTree as ET
        import json
        import re
        
        result_text = ''
        result_text = '\n'.join([str(row) for row in xml_content])

        try:
            root = ET.fromstring(result_text)

            for elem in root.iter(root_name):
                record = {}
                for item in elem:
                    record[item.tag] = item.text
                yield (json.dumps(record),)

        except:
            return None




# U40.	Top: Processes one group at a time and returns the top N values of an attribute 

@udtf(returnType="group_column1: string, group_column2: string, top_s: double")
class AggregateTop:
    def __init__(self):
        self.data= []
        self.top_n = 0
        self.group_col = None
        self.group_col2 = None
        self.value_col = None
    def eval(self, rows: Row, top_n: int, group_col: str,group_col2:str, value_col: str):
        if not self.data:
            self.top_n = top_n
            self.group_col = group_col
            self.group_col2 = group_col2
            self.value_col = value_col
        self.data.append(rows)

    def terminate(self):
        dataset = pd.DataFrame(self.data, columns=[self.group_col,self.group_col2, self.value_col])
        dataset.dropna(inplace=True)
        grouped_df = dataset.groupby(self.group_col).apply(
            lambda x: x.nlargest(self.top_n, self.value_col)
        ).reset_index(drop=True)

        for _, row in grouped_df.iterrows():
            yield tuple(row.values)



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


@udtf(returnType="column1 STRING, column2 STRING,column3 STRING")
class File_q7:
    def eval(self, file_path: str, file_type:str):
        return file(f"{file_path}",file_type)


@udtf(returnType="column1 STRING")
class File_q13:
    def eval(self, file_path: str, file_type:str):
        return file(f"{file_path}",file_type)

@udtf(returnType="column1 STRING, column2 STRING")
class File_q18:
    def eval(self, file_path: str, file_type:str):
        return file(f"{file_path}",file_type)
 