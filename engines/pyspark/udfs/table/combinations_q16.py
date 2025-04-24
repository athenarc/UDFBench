import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
from pyspark.sql.types import *
from pyspark.sql.functions import udtf


# U32.	Combinations(v2 for q16): Reads a json list and returns a table with all the combinations per an integer parameter


@udtf(returnType="pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string,authorpair string")
class Combinations_q16:
    import json
    import itertools
    from itertools import combinations

    def eval(self, vals: Row, N:int):
        if vals:
            if len(vals) == 8:
                try:
                    name_list = json.loads(vals[7])
                    for name_per in itertools.combinations(name_list, N):
                        yield (vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],json.dumps(list(name_per)),)
                except:
                    yield (vals[0],vals[1],vals[2],vals[3],vals[4],vals[5],vals[6],'[]')
            else:
                yield  (None,None,None,None,None,None,None,None)
        else:
            yield  (None,None,None,None,None,None,None,None)


