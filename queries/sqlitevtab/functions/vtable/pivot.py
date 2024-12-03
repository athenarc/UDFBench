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
        # pivoted_df = pivoted_df.sort_index(axis=1)
        # print(pivoted_df)
        
        for row in pivoted_df.itertuples(index=False):
            yield tuple(row)
        # for _,row in pivoted_df.iterrows():
        #     yield tuple(row.values)

    except :
        raise
        return None



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


