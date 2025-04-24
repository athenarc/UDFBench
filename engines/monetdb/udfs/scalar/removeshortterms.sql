

-- U24.	Removeshortterms:  processes a json list where each value contains more than one tokens and removes tokens with length less than 3 chars 

CREATE or replace FUNCTION removeshortterms(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    import json
    def jremoveshortwords(jval):
        def removeshortwords(name):
            return " ".join([word for word in name.split(' ') if len(word) > 2])

        try:
            return json.dumps([removeshortwords(name) for name in json.loads(jval)])
        except:
            return "[]"


    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jremoveshortwords(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([jremoveshortwords(input) if input is not None and input!='-' else numpy.nan ], dtype=object)


};