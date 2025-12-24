import json
import pyarrow as pa

# U19.	Jsort: processes a json list and returns a sorted json list 
def _jsort(jval:str)->str:
    try:
        return json.dumps(sorted(json.loads(jval)))
    except:
        return "[]"


def jsort(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_jsort(row))
    return pa.array(res, type=pa.string())
