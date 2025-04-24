
import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

   
# U40.	Top: Processes one group at a time and returns the top N values of an attribute 

@udtf(returnType="group_column1: string, group_column2: string, top_s: double")
class AggregateTop:
    def __init__(self):
        self.data= []
        self.top_n = 0
        self.group_col = None
        self.group_col2 = None
        self.value_col = None
    def eval(self, rows: Row, top_n: int, group_col: str,group_col2:str, value_col: str):
        if not self.data:
            self.top_n = top_n
            self.group_col = group_col
            self.group_col2 = group_col2
            self.value_col = value_col
        self.data.append(rows)

    def terminate(self):
        dataset = pd.DataFrame(self.data, columns=[self.group_col,self.group_col2, self.value_col])
        dataset.dropna(inplace=True)
        grouped_df = dataset.groupby(self.group_col).apply(
            lambda x: x.nlargest(self.top_n, self.value_col)
        ).reset_index(drop=True)

        for _, row in grouped_df.iterrows():
            yield tuple(row.values)

