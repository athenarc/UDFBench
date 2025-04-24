import os
import importlib
import duckdb
import os
import pandas as pd
import numpy as np

class Table:
    def __init__(self,conn,external_path=None):
        self.con = conn.cursor()
        self.external_path = external_path

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith(".py") and filename not in {"__init__.py"}:
        module_name = filename[:-3]
        module = importlib.import_module(f".{module_name}", package=__name__)

        for attr_name in dir(module):
            func = getattr(module, attr_name)
            if callable(func):
                setattr(Table, attr_name, func)

__all__ = ["Table"]
