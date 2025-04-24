
import duckdb
import os
import pandas as pd
import numpy as np


#  U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

def strsplitv(self,val:str):
    def strsplitv_loc(val):
        try:
            return val.split()   
        except:
            return []
    return [{"term":strsplitv_loc(str(x))} if x.is_valid else ({"term":None}) for x in val]


