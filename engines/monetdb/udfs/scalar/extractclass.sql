-- U5.	Extractclass: extracts class from string with format funder::class::projectid 

CREATE or replace FUNCTION extractclass(input string)
RETURNS STRING
LANGUAGE PYTHON
{

    def extractclass(project):
        try:
            return str(project.split("::")[1])
        except:
            return ""


    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractclass(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [extractclass(input) if input  is not None and input!='-' else numpy.nan],dtype=object)

};
