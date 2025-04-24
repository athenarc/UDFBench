-- U12.  Extractyear : Reads a date (as a string) and extracts an integer with the year


CREATE or replace FUNCTION extractyear(input string)
RETURNS INT
LANGUAGE PYTHON
{
    def extractyear(arg):
        try:
            return int(arg[:arg.find('-')])
        except:
            return -1

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractyear(x) if x is not None and x!='-' else None for x in input],dtype=numpy.float64 )

    else:
        return numpy.array( [extractyear(input) if input is not None and input!='-' else None],dtype=numpy.float64 )

};

