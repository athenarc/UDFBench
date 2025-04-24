-- U18.	Jsonparse: Parses a json dict per time and returns a string with the value

CREATE OR REPLACE FUNCTION jsonparse(input string,key1 string) 
RETURNS string
LANGUAGE PYTHON {

    import json

    def jsonparse(jval,key1):
        try:
            data = json.loads(jval)
            if isinstance(data, list):
                for item in data:
                    return item.get(key1)
                return numpy.nan
            elif isinstance(data, dict):
                return data.get(key1)
            else:
                return numpy.nan
        except:
            return numpy.nan

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jsonparse(x,key1) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)
    else:
        return numpy.array([jsonparse(input,key1) if input is not None and input!='-' else numpy.nan],dtype=object)

};


