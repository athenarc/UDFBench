import pyarrow as pa

# U8.	Extractfunder: extracts funder from string with format funder::class::projectid
def _extractfunder(project:str)->str:
    if project:
        try:
            if '::' in project:
                return project.split("::")[0]
            else:
                return None
        except:
            return None
    else:
        return None




def extractfunder(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractfunder(row))
    return pa.array(res, type=pa.string())

