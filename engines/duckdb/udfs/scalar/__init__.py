import os
import importlib
import re
import pyarrow as pa
import pandas as pd
import time
import json
import math
import heapq
import random
from collections import Counter


class Scalar:
    def __init__(self):
        pass

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename not in {"__init__.py"}:
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)

        for attr_name in dir(module):
            # if attr_name.startswith("aggregate_"):
            func = getattr(module, attr_name)
            if callable(func):
                setattr(Scalar, attr_name, func)

__all__ = ["Scalar"]
