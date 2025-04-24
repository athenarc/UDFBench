import duckdb
import numpy as np
import pyarrow as pa
import os


# U27.	Count(v2): Calculates count  with group by

def aggregate_count_v2(self,subquery:str,value_column:str,group_column=None)->float:
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    try:
        table = self.con.sql(str(subquery)).fetchdf()
        table = table.where(pd.notnull(table), None)
        table.dropna(inplace=True)
        result = table.groupby(str(group_column))[str(value_column)].agg(['count']).reset_index()
        return result.to_dict('records')
    except:
        return [None]