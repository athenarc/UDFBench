import pyarrow as pa

# U12.  Extractyear : Reads a date (as a string) and extracts an integer with the year

def _extractyear(arg: str) -> int:
    if arg:
        try:
            return int(arg[:arg.find('-')])
        except:
            return -1
    else:
        return None


def extractyear(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractyear(row))
    return pa.array(res, type=pa.int32())
