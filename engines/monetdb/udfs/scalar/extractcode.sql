-- U6.	Extractcode: Processes a structured string containing the funder’s id, the funding class and the project id, and extracts the project id

CREATE or replace FUNCTION extractcode(input string)
RETURNS string
LANGUAGE PYTHON
{
    
    def extractcode(project):
        try:
            return project.split("::")[2]
        except:
            return numpy.nan

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractcode(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [extractcode(input) if input is not None and input!='-' else numpy.nan],dtype=object)

};
