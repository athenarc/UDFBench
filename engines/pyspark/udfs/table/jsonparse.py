import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

    

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

