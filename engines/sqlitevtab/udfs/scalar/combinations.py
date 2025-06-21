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
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')

    yield ('pairs',)
    for row in jcombinations(val,numcomb):
            # print(f"Yielding:  {row}")
            yield(row,)



combinations.registered=True
