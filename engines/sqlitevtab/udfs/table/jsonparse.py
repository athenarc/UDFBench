from . import setpath
from . import vtbase
import functions
import csv
import os
import json
import xml.etree.ElementTree as ET
import pandas as pd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

### Classic stream iterator
registered=True

class jsonparse(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)
    self.nonames=True
    self.names=[]
    self.types=[]
    column_name = largs[0]
    key1 = largs[1]
    key2 = largs[2]
    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    cur = envars['db'].cursor()
    cur.execute(query)
    yield (('c1',),('c2',))
    try:
        res = cur.fetchall()
        for data in res:
            rec = json.loads(data[0])
            if isinstance(rec, list):
                for item in rec:
                    yield (item.get(key1),item.get(key2))
            elif isinstance(rec, dict):
                yield (rec.get(key1),rec.get(key2))
            else:
                yield (None,None)
    except:
         raise

def Source():
    return vtbase.VTGenerator(jsonparse)

