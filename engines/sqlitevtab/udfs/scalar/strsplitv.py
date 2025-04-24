

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


def strsplitv(val):
        yield [('c1',)]
        try:
            vals=val.split()
            for v in vals:
                yield  (v,)
        except:
            yield  ['',]
strsplitv.registered = True