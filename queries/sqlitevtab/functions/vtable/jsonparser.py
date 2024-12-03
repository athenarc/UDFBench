"""

.. function:: rowidvt(query:None)

Returns the query input result adding rowid number of the result row.

:Returned table schema:
    Same as input query schema with addition of rowid column.

    - *rowid* int
        Input *query* result rowid.    

Examples::

    >>> table1('''
    ... James   10	2
    ... Mark    7	3
    ... Lila    74	1
    ... ''')
    >>> sql("rowidvt select * from table1")
    rowid | a     | b  | c
    ----------------------
    1     | James | 10 | 2
    2     | Mark  | 7  | 3
    3     | Lila  | 74 | 1
    >>> sql("rowidvt select * from table1 order by c")
    rowid | a     | b  | c
    ----------------------
    1     | Lila  | 74 | 1
    2     | James | 10 | 2
    3     | Mark  | 7  | 3

    Note the difference with rowid table column.

    >>> sql("select rowid,* from table1 order by c")
    rowid | a     | b  | c
    ----------------------
    3     | Lila  | 74 | 1
    1     | James | 10 | 2
    2     | Mark  | 7  | 3
"""
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

class outputs(vtbase.VT):
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
    return vtbase.VTGenerator(outputs)

if not ('.' in __name__):
    """
    This is needed to be able to test the function, put it at the end of every
    new function you create
    """
    import sys
    from . import setpath
    from functions import *
    testfunction()
    if __name__ == "__main__":
        reload(sys)
        sys.setdefaultencoding('utf-8')
        import doctest
        doctest.testmod()


