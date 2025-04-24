

import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

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

