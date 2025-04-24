
import duckdb
import os
import pandas as pd
import numpy as np


#  U42.	Output: Exports the results of a subquery to local storage in various formats and returns a True in success 


def output(self,
    subquery:str,
    output_path:str,
    output_format:str
)->bool:

    import csv
    import json
    import xml.etree.ElementTree as ET
    import pandas as pd
    import duckdb
    def export_to_csv(result, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(result.keys())
            
            # Write data
            for row in zip(*result.values()):
                writer.writerow(row)
        return True

    def export_to_json(result, output_path):
        with open(output_path, 'w') as jsonfile:
            json.dump(list(result), jsonfile, indent=2)
        return True

    def export_to_xml(result, output_path):
        root = ET.Element('root')
        for row in list(result):
            result_element = ET.SubElement(root, 'publications')
            for key, value in row.items():
                ET.SubElement(result_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_path)
        return True



    try:
        cur  = self.con

        result = cur.sql(f"{str(subquery[0])} ;").fetchnumpy()

        out_format= str(output_format[0])
        out_path = str(self.external_path)+'/'+str(output_path[0])
        if out_format.lower() == 'csv':
            return [export_to_csv(result, out_path)]
        elif out_format.lower() == 'json':
            return [export_to_json(result, out_path)]
        elif out_format.lower() == 'xml':
            return [export_to_xml(result, out_path)]
        else:
            return [False]
    
    except:
        return [False]
