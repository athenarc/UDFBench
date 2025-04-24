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

class pivot(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)
    self.nonames=True
    self.names=[]
    self.types=[]
    group_by_column = largs[0]
    pivot_column = largs[1]
    aggregate_function = largs[2]
    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    cur = envars['db'].cursor()
    yield (('pid',), ('datasets',), ('other',), ('publications',), ('software',))
    try:
        data = cur.execute(query)
        data = list(cur.fetchall())
        sch = list(cur.getdescriptionsafe())
        names = [x[0] for x in sch]
        df = pd.DataFrame(data)
        pivoted_df = df.pivot_table(
            index=names.index(group_by_column),
            columns=names.index(pivot_column),
            aggfunc=aggregate_function,
            fill_value=0
        ).reset_index()
    
        for row in pivoted_df.itertuples(index=False):
            yield tuple(row)
     
    except :
        return None

def Source():
    return vtbase.VTGenerator(pivot)
