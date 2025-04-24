
-- U20.	Jsortvalues: processes a json list where each value contains more than one tokens, sorts the tokens in each value 

CREATE or replace FUNCTION jsortvalues(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    import json
    def jsortvalue(jval):
        def sortname(name):
            return " ".join(sorted(name.split(' ')))
        try:
            return json.dumps([sortname(name) for name in json.loads(jval)])
        except:
            return "[]"




    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jsortvalue(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([jsortvalue(input) if input is not None and input!='-' else numpy.nan ], dtype=object)


};