import pyarrow as pa

# U7.	Extractday: Reads a date (as a string) and extracts an integer with the day 

def _extractday(arg: str) -> int:
    if arg:
        try:
            return int(arg[arg.rfind('-')+1:])
        except:
            return -1
    else:
        return None
        
def extractday(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractday(row))
    return pa.array(res, type=pa.int32())
