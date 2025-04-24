
import duckdb
import os
import pandas as pd
import numpy as np

# U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

def combinations(self,jval:str,N:int):
    import json
    import itertools
    from itertools import combinations
    def jcombinations(jval,N=2):
        if jval:
            try:
                name_list = json.loads(str(jval))
                for name_per in itertools.combinations(name_list, int(N)):
                    yield json.dumps([name_per_i for name_per_i in name_per])
            except:
                yield('[]') 
        else:
            yield None 
            
    return [[y for y in  jcombinations(str(arg1),arg2.as_py())] if arg1.is_valid else [None] for arg1,arg2 in zip(jval,N) ]




