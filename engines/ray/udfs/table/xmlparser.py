import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc
import json
import xml.etree.ElementTree as ET


#  U38.	Xmlparser :  Parses xml input and returns a table 
def xmlparser(batch:pa.Table,root_name:str="publication")->pa.Table:
    xml_content = batch["line"].to_pylist()
    result_text = ''
    result_text = '\n'.join([str(row) for row in xml_content])
    rows =[]

    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(root_name):
            record = {}
            for item in elem:
                record[item.tag] = item.text
            rows.append(json.dumps(record),)
        return pa.table({
        "record": pa.array(rows, type=pa.string()),
    })
    except:
        return None