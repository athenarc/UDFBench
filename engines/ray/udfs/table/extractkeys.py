
import json
import ray
import pyarrow as pa
from ray.data.datatype import DataType
from ray.data.expressions import udf, col
import pyarrow.compute as pc

#  U33.	Extractkeys: Selects keys from xml parsed input 

def _extractkeys(jval,key1,key2):
    try:
        data = json.loads(jval)
        if isinstance(data, list):
            for item in data:
                yield  (item.get(key1), item.get(key2))
        elif isinstance(data, dict):
            yield  (data.get(key1),data.get(key2))
        else:
            yield (None,None)
    except:
        yield (None,None)

def extractkeys(batch: pa.Table, key1: str="publicationdoi", key2: str="fundinginfo")-> pa.Table:
    x = batch["record"]

    res = []
    res2 = []

    for row in x.to_pylist():
      for (val1,val2) in _extractkeys(row,key1,key2):
        res.append(val1)
        res2.append(val2)
    return pa.table({
        key1: pa.array(res, type=pa.string()),
        key2: pa.array(res2, type=pa.string()),
    })

    


