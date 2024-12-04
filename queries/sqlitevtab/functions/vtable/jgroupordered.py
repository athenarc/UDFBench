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

class jgroupordered(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    def iterators(df):
      for _, row in df.iterrows():
          yield tuple(row.values)
    largs, dictargs = self.full_parse(parsedArgs)
    self.nonames=True
    self.names=[]
    self.types=[]
    order_by_col = largs[0]
    count_col = largs[1]
    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    cur = envars['db'].cursor()

    yield (('term',), ('docid',), ('tf',), ('jcount',) )
    rows = cur.execute(query)
    rows = cur.fetchall()
    sch = list(cur.getdescriptionsafe())
    colnames = [x[0] for x in sch]
    data = list(rows)
    cur.close()
    # print("in jgroup")
    df = pd.DataFrame(data)
    df['jcount'] = df.groupby([colnames.index(order_by_col)])[colnames.index(count_col)].transform('size')
    it = iterators(df)
    while True:
       yield next(it)


def Source():
    return vtbase.VTGenerator(jgroupordered)

