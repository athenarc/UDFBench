
-- U17.	Jsoncount: Returns the length of a json list


CREATE or replace FUNCTION jsoncount(input string)
RETURNS INT
LANGUAGE PYTHON
{
    import json
    import pandas as pd
    def jsoncount(jval):
        try:
            if jval[0]=='[':
                tot_json = json.loads(jval)
                return int(len(tot_json))
            else:
                return 1
        except:
            return None

    if isinstance(input, str):
        result = jsoncount(input)
        if result is None:
            return pd.DataFrame([None])
        else:
            return pd.DataFrame([result])
    else:
        rows = []
        for x in input:
            row = jsoncount(x)
            if row:
                rows.append(row)
            else:
                rows.append(None)
        return pd.DataFrame(rows)
};
