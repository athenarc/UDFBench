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

def extractfromdate(arg):
 yield  ('extractyear', 'extractmonth', 'extractday')
 try:
            yield (int(arg[:arg.find('-')]), int(arg[arg.find('-')+1:arg.rfind('-')]), int(arg[arg.rfind('-')+1:]))

 except:
            yield (-1,-1,-1)

extractfromdate.registered = True
