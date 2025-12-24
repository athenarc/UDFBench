
import json
import pyarrow as pa


# U24.	Removeshortterms:  processes a json list where each value contains more than one tokens and removes tokens with length less than 3 chars 
def _removeshortterms(jval:str)->str:
    def removeshortwords(name):
        return " ".join([word for word in name.split(' ') if len(word) > 2])
    try:
        return json.dumps([removeshortwords(name) for name in json.loads(jval)])
    except:
        return "[]"



def removeshortterms(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_removeshortterms(row))
    return pa.array(res, type=pa.string())