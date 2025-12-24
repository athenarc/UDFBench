import json
import pyarrow as pa


# U18.	Jsonparse: Parses a json dict per time and returns a string with the value

def _jsonparse(json_content: str,key1: str)->str:
   
    try:
        data = json.loads(json_content)
        if isinstance(data, list):
            for item in data:
                return item.get(key1)
        elif isinstance(data, dict):
            return data.get(key1)
        else:
            return None
    except:
        return None


def jsonparse(arr: pa.Array, key: str = 'value') -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_jsonparse(row,key))
    return pa.array(res, type=pa.string())
