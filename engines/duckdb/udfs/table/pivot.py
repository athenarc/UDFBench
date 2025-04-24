

import duckdb
import os
import pandas as pd
import numpy as np

# U39.	Pivot: Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset. It returns one tuple per input group

def pivot(self,
    subquery:str,
    group_by_column:str,  
    pivot_column:str,      
    aggregate_function:str
):

    import pandas as pd
    try:
        cur  = self.con
        df = cur.sql(f"{str(subquery[0])};").fetchdf()
        
        group_by_col=str(group_by_column[0])
        pivot_col=str(pivot_column[0])
        aggr_func = str(aggregate_function[0])
        
        pivoted_df = df.pivot_table(
            index=group_by_col,
            columns=pivot_col,
            aggfunc=aggr_func,
            fill_value=0
        ).reset_index()
        return [pivoted_df.to_dict('records')]
    except:
        return [None]