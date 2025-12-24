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


# U32.	Combinations(v2 for q16): Reads a json list and returns a table with all the combinations per an integer parameter


def combinations_q16(batch: pa.Table, N: int = 2) -> pa.Table:
    x = batch["authorlist"]
    target_col = pc.if_else(pc.is_valid(x), x, pa.scalar("[]", pa.string()))

    ids = []
    combos = []
    pubdate = []
    projectstart = []
    projectend = []
    funder = []
    class_ = []
    projectid = []
    for i, val in enumerate(target_col.to_pylist()):

        try:

          vals = json.loads(val) if val!="[]" else []  
          
          for pair in itertools.combinations(vals, N):
              ids.append(batch["artifactid"][i])
              pubdate.append(batch["date"][i])
              projectstart.append(batch["projectstart"][i])
              projectend.append(batch["projectend"][i])
              funder.append(batch["funder"][i])
              class_.append(batch["class"][i])
              projectid.append(batch["projectid"][i])


              combos.append(json.dumps(pair))
        except Exception:
            continue
    return pa.table({"pubid": pa.array(ids, pa.string()),
    "pubdate": pa.array(pubdate, pa.string()),
    "projectstart": pa.array(projectstart, pa.string()),
    "projectend": pa.array(projectend, pa.string()),
    "funder": pa.array(funder, pa.string()),
    "class": pa.array(class_, pa.string()),
    "projectid": pa.array(projectid, pa.string()),
    "authorpair": pa.array(combos, pa.string())})
