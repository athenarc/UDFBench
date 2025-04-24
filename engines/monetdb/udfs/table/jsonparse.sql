-- U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values


CREATE OR REPLACE FUNCTION jsonparse(subquery STRING,key1  STRING, key2 STRING) 
RETURNS TABLE (publicationdoi STRING, fundinginfo STRING)
LANGUAGE PYTHON {


    import json
    import pandas as pd
    try:
        rows =[]
        for line in subquery:
            data = json.loads(line)
            if isinstance(data, list):
                for item in data:
                    rows.append((item.get(key1[0]),item.get(key2[0])))
            elif isinstance(data, dict):
                rows.append((data.get(key1[0]),data.get(key2[0])) )
            else:
                rows.append( None,None)
        return pd.DataFrame(rows)

    except:
        return pd.DataFrame({'publicationdoi':[],'fundinginfo':[]})
   
};