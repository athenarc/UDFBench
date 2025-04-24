

import duckdb
import numpy as np
import pyarrow as pa
import os

#  U28. Max: Calculates max date with group by

def aggregate_max(self,subquery:str,value_column:str,group_column=None)->str:
    import numpy as np
    import pyarrow as pa
    import pandas as pd

    try:
        table = self.con.sql(str(subquery)).fetchdf()
        table = table.where(pd.notnull(table), None)
        table.dropna(inplace=True)
        result = table.groupby(str(group_column))[str(value_column)].agg(['max']).reset_index()
        return result.to_dict('records')
    except:
        return [None]