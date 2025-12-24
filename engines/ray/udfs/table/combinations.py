import os
import pandas as pd
import numpy as np
import json
import itertools
from itertools import combinations
import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc


# U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter


def combinations(batch: pa.Table, N: int = 2) -> pa.Table:
    x = batch["authorlist"]
    target_col = pc.if_else(pc.is_valid(x), x, pa.scalar("[]", pa.string()))

    ids = []
    combos = []

    for i, val in enumerate(target_col.to_pylist()):
        try:
            id = batch["artifactid"][i]
            vals = json.loads(val) if val!="[]" else []  

            for pair in itertools.combinations(vals, N):
                ids.append(id)
                combos.append(json.dumps(pair))
        except Exception:
            continue
    return pa.table({"id": pa.array(ids, pa.string()), "combination": pa.array(combos, pa.string())})
