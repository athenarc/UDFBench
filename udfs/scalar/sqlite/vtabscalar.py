# coding: utf-8
from . import setpath
import re
import functions
import unicodedata
import hashlib
import itertools
from collections import deque
import json
import itertools
import math
from collections import OrderedDict

def combinations(val,numcomb):
    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield [json.dumps(name_i) for name_i in name_per]

        except:
            yield('[]')

    yield ('pairs',)
    for row in jcombinations(val,numcomb):
            # print(f"Yielding:  {row}")
            yield(row)



combinations.registered=True


def combinations_fused(fundingstring,val,numcomb):

    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]') 


    def extractfundingstring(project):
        try:
            listproject = project.split("::")
            return  listproject[0], listproject[1], listproject[2]
        except Exception as e:
            return None,None,None


    def removeshortwords(name):
        return " ".join([word for word in name.split(' ') if len(word) > 2])
    
    def sortname(name):
        return " ".join(sorted(name.split(' ')))


    def jfusedudfs(jval):
        if jval:
            try:
                jval = json.loads(jval)
                jval = [name.lower() for name in jval]
                jval = [removeshortwords(name) for name in jval]
                jval = [sortname(name) for name in jval]
                jval = sorted(jval)

                return json.dumps(jval)
            except:
                return "[]"
        else:
            return None

    yield ('funder','class','projectid','pairs',)
    (funder, _class, projectid) = extractfundingstring(fundingstring)

    for row in jcombinations(jfusedudfs(val), numcomb):
        yield (funder,_class, projectid,row)

combinations_fused.registered=True

def extractkeys(jval, key1, key2):
    yield ('key1','key2')
    try:
        data = json.loads(jval)

        if isinstance(data, list):
            for item in data:
                yield (item.get(key1),item.get(key2))

        elif isinstance(data, dict):
            # Extract values dynamically for all keys in the dictionary
            yield (data.get(key1),data.get(key2))

        else:
            yield (None,None)

    except Exception as e:
        return (None,None)

extractkeys.registered = True

def extractfromdate(arg):
 yield  ('extractyear', 'extractmonth', 'extractday')
 try:
            yield (int(arg[:arg.find('-')]), int(arg[arg.find('-')+1:arg.rfind('-')]), int(arg[arg.rfind('-')+1:]))

 except:
            yield (-1,-1,-1)

extractfromdate.registered = True


def strsplitv(val):
        yield [('c1',)]
        try:
            vals=val.split()
            for v in vals:
                yield  (v,)
        except:
            yield  ['',]
strsplitv.registered = True