import os
import importlib
import duckdb
import numpy as np
import pyarrow as pa
import os


class Aggregate:
    def __init__(self,con):
        self.con = con.cursor()

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename not in {"__init__.py"}:    
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)

        for attr_name in dir(module):
            func = getattr(module, attr_name)
            if callable(func):
                setattr(Aggregate, attr_name, func)

__all__ = ["Aggregate"]
