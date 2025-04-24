
import duckdb
import os
import pandas as pd
import numpy as np

# U30.	Extractfromdate(v2): Reads a date (as a string) and returns 3 column values (year, month, day)


def extractfromdate(self,arg:str):

    def extractdate(arg):
        try:
            return {"year":int(arg[:arg.find('-')]),
                    "month":int(arg[arg.find('-')+1:arg.rfind('-')]),
                    "day":int(arg[arg.rfind('-')+1:])
            }
        except:
            return {"year":-1,
                    "month":-1,
                    "day":-1
            }

    return [(extractdate(str(x))) if x.is_valid else ({"year":None,"month":None,"day":None}) for x in arg]

