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


### Classic stream iterator
registered=True

class outputs(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    largs, dictargs = self.full_parse(parsedArgs)

    self.nonames=True
    self.names=[]
    self.types=[]
    output_path = largs[0]
    output_format = largs[1]
    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    yield ('c1',)
    cur = envars['db'].cursor()
    def execute_subquery(query, cur):
        result = list(cur.execute(query))
        return result

    def export_to_csv(result, output_path):
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            #csv_writer.writerow(result[0].keys())
            for row in result:
                csv_writer.writerow(row)
        return True

    def export_to_json(result, output_path):
        with open(output_path, 'w') as jsonfile:
            json.dump(list(result), jsonfile, indent=2)
        return True

    def export_to_xml(result, output_path):
        root = ET.Element('root')
        for row in list(result):
            result_element = ET.SubElement(root, 'publication')
            for key, value in row.items():
                ET.SubElement(result_element, key).text = str(value)

        tree = ET.ElementTree(root)
        tree.write(output_path)
        return True

    try:
        result = execute_subquery(query, cur)

        if output_format.lower() == 'csv':
            export_to_csv(result, output_path)
        elif output_format.lower() == 'json':
            export_to_json(result, output_path)
        elif output_format.lower() == 'xml':
            export_to_xml(result, output_path)
        yield (1,)
    except Exception as e:
        raise
        yield False




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


