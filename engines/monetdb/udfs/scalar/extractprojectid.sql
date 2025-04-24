
-- U11.	Extractprojectid: Processes a text snippet and extracts a 6 digit project identifier 


CREATE or replace FUNCTION extractprojectid(input string)
RETURNS string
LANGUAGE PYTHON
{
    import re
    def extractprojid(inp):
        try:
            return re.findall(r"(?<!\d)[0-9]{6}(?!\d)",inp)[0]
        except: return ''

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([extractprojid(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [extractprojid(input) if input is not None and input!='-' else numpy.nan],dtype=object)

};
