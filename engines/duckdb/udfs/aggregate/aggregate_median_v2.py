import duckdb
import numpy as np
import pyarrow as pa
import os


#  U29.	Median(v2): Calculates median with group by

def aggregate_median_v2(self,subquery:str,value_column:str,group_column=None)->float:
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    try:
        table = self.con.sql(str(subquery)).fetchdf()
        table = table.where(pd.notnull(table), None)
        table.dropna(inplace=True)
        result = table.groupby(str(group_column))[str(value_column)].agg(['median']).reset_index()
        return result.to_dict('records')
    except:
        return [None]