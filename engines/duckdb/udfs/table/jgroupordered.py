import duckdb
import os
import pandas as pd
import numpy as np



#  U35.	jgroupordered: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

def jgroupordered(self,subquery:str, order_by_col:str,count_col:str):


    try:
        con_func = self.con
        df = con_func.sql(f"{str(subquery[0])};").fetchdf()

        df['jcount'] = df.groupby([str(order_by_col[0])])[str(count_col[0])].transform('size')
        df.dropna(inplace=True)  
        return [df.to_dict('records')]
    except:
        return [None]

