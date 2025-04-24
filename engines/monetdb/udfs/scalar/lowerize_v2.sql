-- U23.	Lowerize(v2): processes a json list and returns a lower json list

CREATE or replace FUNCTION lowerize_v2(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    import json
    def jlower(jval):
        try:
            return json.dumps([name.lower() for name in json.loads(jval)])
        except:
            return  "[]" 


    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jlower(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([jlower(input) if input is not None and input!='-' else numpy.nan ], dtype=object)

};