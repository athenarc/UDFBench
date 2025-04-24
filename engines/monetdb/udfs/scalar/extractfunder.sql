-- U8.	Extractfunder: extracts funder from string with format funder::class::projectid

CREATE or replace FUNCTION extractfunder(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    def extractfunder(project):
        try:
            if '::' in project:
                return str(project.split('::')[0])
            else:
                return numpy.nan
        except:
            return numpy.nan



    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractfunder(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [extractfunder(input) if input is not None and input!='-' else numpy.nan],dtype=object)

};
