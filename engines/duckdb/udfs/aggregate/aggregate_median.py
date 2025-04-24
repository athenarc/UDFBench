import duckdb
import numpy as np
import pyarrow as pa
import os

#  U29.	Median: Calculates median
def aggregate_median(self,subquery:str,value_column:str)->float:
    import numpy as np
    import pandas as pd
    import pyarrow as pa

    try:
        table = self.con.sql(str(subquery)).fetchdf()
        value_column = str(value_column)
        median_val = table[value_column].median() if not table[value_column].isnull().all() else np.nan

        return median_val
    except:
        return None