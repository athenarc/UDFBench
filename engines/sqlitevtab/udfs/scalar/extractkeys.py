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