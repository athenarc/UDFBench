import ray
import pyarrow as pa

# U6.	Extractcode: Processes a structured string containing the funder’s id, the funding class and the project id, and extracts the project id

def _extractcode(project: str)->str:
    if project:
        try:
            return project.split("::")[2]
        except:
            return None
    else:
        return None


def extractcode(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_extractcode(row))
    return pa.array(res, type=pa.string())
