-- U9.	Extractid: extracts project id from string with format funder::class::projectid 

CREATE or replace FUNCTION extractid(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    def extractid(project):
        try:
            if '::' in project:
                return str(project.split('::')[2])
            else:
                return numpy.nan
        except:
            return numpy.nan

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractid(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [extractid(input) if input is not None and input!='-' else numpy.nan],dtype=object)


};
