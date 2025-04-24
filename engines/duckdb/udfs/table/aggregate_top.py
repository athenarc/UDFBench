
import duckdb
import os
import pandas as pd
import numpy as np

# U40.	Top: Processes one group at a time and returns the top N values of an attribute 

def aggregate_top(self,subquery:str,group_col:str,value_col:str,top_n:int):
    import pandas as pd
    import duckdb
    try:
        cur  = self.con

        df = cur.sql(f"{str(subquery[0])};").fetchdf()
        res = df.groupby(str(group_col[0])).apply(lambda x: x.nlargest(int(top_n[0].as_py()), str(value_col[0]))).reset_index(drop=True)
        res.dropna(inplace=True)  
        return [res.to_dict('records')]
    except:
        return [None]
