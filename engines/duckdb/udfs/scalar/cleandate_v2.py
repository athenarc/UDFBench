import pyarrow as pa


# U3.	Cleandate(v2):Process a chunk at the time. Reads each date and converts it to a common format if it is not, handles also dirty dates

def cleandate_v2(self,args:pa.array) -> pa.array:
    try:
        args_list =args.to_pylist()
        return [self.cleandate(arg) for arg in args_list]
    except: 
        return [None]