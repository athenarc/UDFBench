
import duckdb
import os
import pandas as pd
import numpy as np

#  U33.	Extractkeys: Selects keys from xml parsed input 


def extractkeys(self,jval:str,key1:str,key2:str):
    import json

    def extractkeys(jval,key1,key2):
        try:
            data = json.loads(jval)

            if isinstance(data, list):
                for item in data:
                    return  ({"key1":item.get(key1),"key2":item.get(key2)})
            elif isinstance(data, dict):
                return  ({"key1":data.get(key1),"key2":data.get(key2)})
            else:
                return  ({"key1":None,"key2":None})
        except:
            return ({"key1":None,"key2":None})

    
    return [(extractkeys(str(val),str(k1),str(k2))) if val.is_valid else ({"key1":None,"key2":None}) for val,k1,k2 in zip(jval,key1,key2)]
