
import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf



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


