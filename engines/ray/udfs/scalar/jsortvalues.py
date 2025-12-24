import json
import pyarrow as pa

# U20.	Jsortvalues: processes a json list where each value contains more than one tokens, sorts the tokens in each value 

def _jsortvalues(jval:str)->str:
    def sortname(name):
        return " ".join(sorted(name.split(' ')))
    try:
        return json.dumps([sortname(name) for name in json.loads(jval)])
    except:
        return "[]"

def jsortvalues(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_jsortvalues(row))
    return pa.array(res, type=pa.string())

