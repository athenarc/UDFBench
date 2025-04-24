-- U7.	Extractday: Reads a date (as a string) and extracts an integer with the day 

CREATE or replace FUNCTION extractday(input string)
RETURNS INT
LANGUAGE PYTHON
{
    def extractday(arg):
        try:
            return int(arg[arg.rfind('-')+1:])
        except:
            return -1

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractday(x) if x is not None and x!='-' else None for x in input],dtype=numpy.float64 )

    else:
        return numpy.array( [extractday(input) if input is not None and input!='-' else None],dtype=numpy.float64 )
        

};
