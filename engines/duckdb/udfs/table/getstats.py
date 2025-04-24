import duckdb
import os
import pandas as pd
import numpy as np

# U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

def getstats(self,subquery:str):

    import numpy as np
    import pyarrow as pa
    import  duckdb

    cur  = self.con

    table = cur.sql(str(subquery[0])).fetchdf()
    avg_val =  np.NaN if table['authors'].isnull().all()  else np.nanmean(table.authors)
    median_val = np.NaN if table['authors'].isnull().all() else np.nanmedian(table.authors)
    return ({'avg':avg_val,'median':median_val},)
