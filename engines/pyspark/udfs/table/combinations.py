import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf


# U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

@udtf(returnType="authorpairs: string")
class Combinations:
    def eval(self, vals: str, N:int):
        # for val in vals:
            if vals:
                try:
                    name_list = json.loads(vals[0])
                    for name_per in itertools.combinations(name_list, N):
                        yield (json.dumps(list(name_per)),)
                except:
                    yield ('[]')
            else:
                yield None 

