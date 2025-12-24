import pyarrow as pa

def _extractid(project:str)->str:
    if project:
        try:
            return project.split("::")[2]
        except:
            return None
    else:
        return None



def extractid(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractid(row))
    return pa.array(res, type=pa.string())