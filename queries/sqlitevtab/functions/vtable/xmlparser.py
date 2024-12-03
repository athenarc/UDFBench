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
import re

### Classic stream iterator
registered=True

class xmlparser(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)


    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']

    cur = envars['db'].cursor()
    cur.execute(query)
    sch = list(cur.getdescriptionsafe())
    sch = [x[0] for x in sch]
    self.nonames=True
    self.names=[]
    self.types=[]
    root_name = largs[0]
    column_name = largs[1]
    result_text = ''
    result_text = '\n'.join([str(row[sch.index(column_name)]) for row in cur.fetchall()])
    yield [('c1',)]
    try:
        # Parse the XML content
        root = ET.fromstring(result_text)

        # Iterate through XML elements and yield records
        for elem in root.iter(root_name):
            record = {}
            # Extract values dynamically for all attributes in the element
            for item in elem:
                record[item.tag] = item.text
            yield (json.dumps(record),)

    except Exception as e:
        return None



def Source():
    return vtbase.VTGenerator(xmlparser)

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


