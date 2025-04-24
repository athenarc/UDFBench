-- U33.	Extractkeys: Selects keys from xml parsed input 

CREATE OR REPLACE FUNCTION extractkeys(jval STRING,key1 STRING,key2 STRING) 
RETURNS TABLE (
    publicationdoi STRING,
    fundinginfo STRING
) 
LANGUAGE PYTHON {

    import json
    import pandas as pd 

    def extract_keys(jval,key1,key2):
        try:
            data = json.loads(jval)

            if isinstance(data, list):
                for item in data:
                    yield (item.get(key1),item.get(key2))

            elif isinstance(data, dict):
                yield (data.get(key1),data.get(key2))

            else:
                yield (None,None)

        except:
            yield (None,None)
        
    try:

        if type(jval)==numpy.ndarray or type(jval)==numpy.ma.core.MaskedArray:

            res=  pd.DataFrame(((y1,y2) for arg1,arg2,arg3 in zip(jval,key1,key2) for y1,y2 in extract_keys(arg1,arg2,arg3 )))
        else:
            res = pd.DataFrame(((y1,y2)  for y1,y2 in extract_keys(jval,key1,key2)))
        
        if not res.empty:
            return res
        else:
           return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})


    except:
        return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})


};