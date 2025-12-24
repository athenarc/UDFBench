import pyarrow as pa

# U10. Extractmonth: Reads a date (as a string) and extracts an integer with the month

def _extractmonth(arg: str) -> int:
    if arg:
        try:
            return int(arg[arg.find('-')+1:arg.rfind('-')])
        except:
            return -1
    else:
        return None


        
def extractmonth(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractmonth(row))
    return pa.array(res, type=pa.int32())
