import duckdb
import numpy as np
import pyarrow as pa
import os

#  U26.	Avg: Calculates average

def aggregate_avg(self,subquery:str,value_column:str)->float:
    import numpy as np
    import pyarrow as pa
    import pandas as pd

    try:
        table = self.con.sql(str(subquery)).fetchdf()
        value_column = str(value_column)
        avg_val = table[value_column].mean() if not table[value_column].isnull().all() else np.nan

        return avg_val
    except:
        return None
