import duckdb
import numpy as np
import pyarrow as pa
import os

#  U27.	Count: Calculates count 

def aggregate_count(self,subquery:str,value_column:str)->int:
    import numpy as np
    import pandas as pd
    import pyarrow as pa
    try:
        table = self.con.sql(str(subquery)).fetchdf()
        table = table.where(pd.notnull(table), None)
        count_vals =  int(table[str(value_column)].count())
        return count_vals
    except:
        return None