import json
import pyarrow as pa

# U23. Lowerize: Converts to lower case the input text 
def _lowerize(val: str)->str:
    if val:
        try:
            return val.lower()
        except:
            return ''
    else:
        return None


def lowerize(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_lowerize(row))
    return pa.array(res, type=pa.string())
