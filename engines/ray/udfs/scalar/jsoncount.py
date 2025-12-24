
import json
import pyarrow as pa


# U17.	Jsoncount: Returns the length of a json list
def _jsoncount(jval: str) -> int:
    try:
        if jval[0]=='[':
            tot_json = json.loads(jval)
            return int(len(tot_json))
        else:
            return 1
    except:
        return None


def jsoncount(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_jsoncount(row))
    return pa.array(res, type=pa.int32())
