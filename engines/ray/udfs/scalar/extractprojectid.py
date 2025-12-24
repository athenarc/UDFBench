import re
import pyarrow as pa

# U11.	Extractprojectid: Processes a text snippet and extracts a 6 digit project identifier 

def _extractprojectid(input: str)->str:

    if input:
        try:
            return re.findall(r"(?<!\d)[0-9]{6}(?!\d)",input)[0]
        except: return ''
    else:
        return None


def extractprojectid(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractprojectid(row))
    return pa.array(res, type=pa.string())