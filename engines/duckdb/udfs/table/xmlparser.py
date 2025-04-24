

import duckdb
import os
import pandas as pd
import numpy as np

#  U38.	Xmlparser :  Parses xml input and returns a table 


def xmlparser(self,subquery:str,root_name:str):

    import xml.etree.ElementTree as ET
    import json
    import pandas as pd

    result_text = ''
    result_text = '\n'.join([str(row) for row in subquery])
    rows =[]
    try:
        root = ET.fromstring(result_text)

        for elem in root.iter(str(root_name[0])):
            record = {}
            for item in elem:
                record[item.tag] = item.text

            rows.append(json.dumps(record),)
        return [rows]
    except:
        return[None]
