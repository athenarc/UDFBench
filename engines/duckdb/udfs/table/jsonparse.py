
import duckdb
import os
import pandas as pd
import numpy as np


#  U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values


def jsonparse(self,json_content: str,key1: str,key2: str):
    import json
    try:
        data = json.loads(json_content)
        if isinstance(data, list):
            for item in data:
                return (item.get(key1),item.get(key2))
        elif isinstance(data, dict):
                return (data.get(key1),data.get(key2))
        else:
            return (None,None)
    except:
        return (None,None)
