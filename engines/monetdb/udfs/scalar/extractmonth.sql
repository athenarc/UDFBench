-- U10. Extractmonth: Reads a date (as a string) and extracts an integer with the month

CREATE or replace FUNCTION extractmonth(input string)
RETURNS INT
LANGUAGE PYTHON
{
    def extractmonth(arg):
        try:
            return int(arg[arg.find('-')+1:arg.rfind('-')])
        except:
            return -1

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractmonth(x) if x is not None and x!='-' else None for x in input],dtype=numpy.float64 )

    else:
        return numpy.array( [extractmonth(input) if input is not None and input!='-' else None],dtype=numpy.float64 )

};
