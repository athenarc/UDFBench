import ray
import pyarrow as pa

# U5.	Extractclass: extracts class from string with format funder::class::projectid 
def _extractclass(project:str)->str:
    if project:
        try:
            return project.split("::")[1]
        except:
            return None
    else:
        return None



def extractclass(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractclass(row))
    return pa.array(res, type=pa.string())
