

-- U19.	Jsort: processes a json list and returns a sorted json list 

CREATE or replace FUNCTION jsort(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    import json
    def jsort(jval):
        try:
            return json.dumps(sorted(json.loads(jval)))
        except:
            return "[]"


    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jsort(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([jsort(input) if input is not None and input!='-' else numpy.nan ], dtype=object)

};

