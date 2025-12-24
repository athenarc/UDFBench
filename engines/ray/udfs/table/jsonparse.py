import json
import pyarrow as pa
import pyarrow.compute as pc



#  U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values
def _jsonparse(json_content: str,key1: str,key2: str):
    try:
        data = json.loads(json_content)
        if isinstance(data, list):
            for item in data:
                return (item.get(key1),item.get(key2))
        elif isinstance(data, dict):
                return (data.get(key1),data.get(key2))
        else:
            return (None,None)
    except:
        return (None,None)

def jsonparse(batch: pa.Table, key1: str="publicationdoi", key2: str="fundinginfo")-> pa.Table:
    x = batch["line"]
    target_col = pc.if_else(pc.is_valid(x), x, pa.scalar("[]", pa.string()))
    res = []
    res2 = []

    for row in target_col.to_pylist():
      (val1,val2) = _jsonparse(row,key1,key2)
      res.append(val1)
      res2.append(val2)
    return pa.table({
        key1: pa.array(res, type=pa.string()),
        key2: pa.array(res2, type=pa.string()),
    })