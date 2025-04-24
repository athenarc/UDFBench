from . import setpath
from . import vtbase
import functions
import csv
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd

registered=True
class file(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)

    self.nonames=True
    self.names=[]
    self.types=[]
    file_path = largs[0]
    file_type = largs[1]
    def parse_csv(file_path):
        df = pd.read_csv(file_path,header=None)
        header = 0
        for _, row in df.iterrows():
                if header == 0:
                    yield ('c'+str(d) for x,d in enumerate(row.values))
                    header = 1
                yield tuple(row.values)


    def parse_csv2(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield tuple(row.values())

    def read_json(file_path):
        header = 0
        with open(file_path, 'r') as file:
            first_character = file.read(1)
            file.seek(0)  # Reset the file pointer to the beginning
            if first_character == '[':
                data = json.load(file)
                if isinstance(data, list):
                    for item in data:
                        if header == 0:
                                yield ('c'+str(d) for x,d in enumerate(item.values()))
                                header = 1
                        yield tuple(item.values())
                elif isinstance(data, dict):
                    if header == 0:
                                yield ('c'+str(d) for x,d in enumerate(data.values()))
                                header = 1
                    yield tuple(data.values())
            else:
                for line in file:
                    data = json.loads(line)
                    if isinstance(data, list):
                        for item in data:
                            if header == 0:
                                yield ('c'+str(d) for x,d in enumerate(item.values()))
                                header = 1
                            yield tuple(item.values())
                    elif isinstance(data, dict):
                        if header == 0:
                                yield ('c'+str(d) for x,d in enumerate(data.values()))
                                header = 1
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
        header = 0
        for record in parse_xml(file_path):
            if header==0:
                yield ('c'+str(d) for x,d in enumerate(record))
                header = 1
            yield tuple(record)

    def parse_text(file_path):
        yield [('c1', )]
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

def Source():
    return vtbase.VTGenerator(file)


