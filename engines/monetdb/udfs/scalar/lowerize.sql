-- U23.	Lowerize: Converts to lower case the input text 



CREATE or replace FUNCTION lowerize(input string)
RETURNS string
LANGUAGE PYTHON
{

    def lowerize(val):
        try:
            return val.lower()
        except:
            return ""
    
    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([lowerize(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([lowerize(input) if input is not None and input!='-' else numpy.nan ], dtype=object)



};
