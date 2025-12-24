import pyarrow as pa
import random


# U1. Add_noise : adds gaussian noise to a value and returns a float 
def _addnoise(val:int)->float:

    def add_noise(val, mean=0, std_dev=2):
        if val:       
            noise = random.gauss(mean, std_dev)
            result = float(val) + noise
            return result
        else:
            return None
    try: 
        return add_noise(val)
    except:
        return None


def addnoise(arr: pa.Array) -> pa.Array:
    res = []
    for row in arr.to_pylist():
      res.append(_addnoise(row))
    return pa.array(res, type=pa.float32())
