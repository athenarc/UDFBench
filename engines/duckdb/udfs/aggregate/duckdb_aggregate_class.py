import duckdb
import numpy as np
import pyarrow as pa
import os


class Aggregate:
    def __init__(self,con):
        self.con = con.cursor()