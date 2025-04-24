
CREATE or replace FUNCTION jpack(input string)
RETURNS string
LANGUAGE PYTHON
{
    import json 


    def jpack_text(words):
        try:
            string_split = words.split()
            return json.dumps([word for word in string_split])
        except:
            return ''

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([jpack_text(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([jpack_text(input) if input is not None and input!='-' else numpy.nan ], dtype=object)

};

