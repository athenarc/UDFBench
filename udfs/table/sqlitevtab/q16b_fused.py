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
from collections import defaultdict

### Classic stream iterator
registered=True

class q16b_fused(vtbase.VT):
  def VTiter(self, *parsedArgs, **envars):
    def cleandate(pubdate):
            if pubdate:
                try:
                    if "-" in pubdate:
                        splitnum = pubdate.count('-')
                        pubdate_split = pubdate.split("-")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                        else:
                            return None
                    elif "/" in pubdate:
                        splitnum = pubdate.count('/')
                        pubdate_split = pubdate.split("/")
                        if splitnum ==1:
                            return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                        elif splitnum ==2:
                            return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                        else:
                            return None
                    else:
                        return None
                except:
                    return None
            else:
                return None

    def iterators(df):
      for _, row in df.iterrows():
          yield tuple(row.values)
    largs, dictargs = self.full_parse(parsedArgs)
    self.nonames=True
    self.names=[]
    self.types=[]

    if 'query' not in dictargs:
            raise functions.OperatorError(__name__.rsplit('.')[-1],"No query argument ")
    query=dictargs['query']
    cur = envars['db'].cursor()
    rows = cur.execute(query)
    rows = cur.fetchall()

    cur.close()
    results = defaultdict(lambda: {'authors_during': None, 'authors_before': None, 'authors_after': None})

    for row in rows:
        funder = row[0]
        _class = row[1]
        projectid = row[2]
        
        pstartcleaned = cleandate(row[3])
        pendcleaned = cleandate(row[4])
        pubdatecleaned = cleandate(row[5])
        # print("ok")
        key = (funder, _class, projectid)

        if key not in results:
            results[key]['authors_during'] = None
            results[key]['authors_before'] = None
            results[key]['authors_after'] = None

        if  pubdatecleaned is None:
            continue


        if pstartcleaned and pendcleaned:
            if results[key]['authors_during'] is None:
                results[key]['authors_during'] = 1 if pstartcleaned <= pubdatecleaned <= pendcleaned else None
            else:
                results[key]['authors_during'] += 1 if pstartcleaned <= pubdatecleaned <= pendcleaned else 0

        if pstartcleaned:
            if results[key]['authors_before'] is None:
                results[key]['authors_before'] = 1 if pubdatecleaned < pstartcleaned else None
            else:
                results[key]['authors_before'] += 1 if pubdatecleaned < pstartcleaned else 0

        if pendcleaned:
            if results[key]['authors_after'] is None:
                results[key]['authors_after'] = 1 if pubdatecleaned > pendcleaned else None

            else:
                results[key]['authors_after'] += 1 if pubdatecleaned > pendcleaned else 0

    yield (('funder',), ('_class',), ('projectid',), ('authors_during',), ('authors_before',),('authors_after',) )

    for (funder, _class, projectid), counts in results.items():
      yield (funder, _class, projectid, counts['authors_during'], counts['authors_before'], counts['authors_after'])



def Source():
    return vtbase.VTGenerator(q16b_fused)

