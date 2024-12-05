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
