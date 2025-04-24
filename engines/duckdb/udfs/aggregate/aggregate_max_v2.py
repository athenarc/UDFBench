
import duckdb
import numpy as np
import pyarrow as pa
import os

#  U28. Max(v2): Calculates max date

def aggregate_max_v2(self,subquery:str,value_column:str)->str:
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    try:
        table = self.con.sql(str(subquery)).fetchdf()
        max_val =  np.NaN if table[str(value_column)].isnull().all()  else np.nanmax(table[str(value_column)])
        return max_val
    except:
        return None
