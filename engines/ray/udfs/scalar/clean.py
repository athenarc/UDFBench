import json
import pyarrow as pa

# U2.	Clean: Performs a simple data cleaning task on the string tokens of a json list

def _clean(val: str)->str:
    def removeshortwords(name):
        return " ".join([word for word in name.split(' ') if len(word) > 2])

    def sortname(name):
        return " ".join(sorted(name.split(' ')))

    def cleanpy(val):
        name_list = json.loads(val)
        name_list = [name.lower() for name in name_list]
        name_list = [removeshortwords(name) for name in name_list]
        name_list = [sortname(name) for name in name_list]
        return json.dumps(sorted(name_list))
    
    if val:
        try:
            return cleanpy(val)
        except:
            return "[]"
    else:
        return None


def clean(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_clean(row))
    return pa.array(res, type=pa.string())
