import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf

    
# U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

@udtf(returnType="id string,year int, month int, day int")
class ExtractFromDate:
    def eval(self, args: list):
            (id,arg) = args
            if arg:
                try:
                    yield (id,int(arg[:arg.find('-')]), \
                            int(arg[arg.find('-')+1:arg.rfind('-')]), \
                            int(arg[arg.rfind('-')+1:]))
                    
                except:
                    yield(id, -1,-1,-1)
            else: yield(id,None,None,None)
