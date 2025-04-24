-- U30.	Extractfromdate: Reads a date (as a string) and returns 3 column values (year, month, day)

CREATE or replace FUNCTION extractfromdate(id string, input string)
RETURNS TABLE(id string, extractyear INTEGER, extractmonth INTEGER, extractdate INTEGER)
LANGUAGE PYTHON
{

    def extractfromdate(arg):
        try:
            return int(arg[:arg.find('-')]), \
                    int(arg[arg.find('-')+1:arg.rfind('-')]), \
                    int(arg[arg.rfind('-')+1:])
            
        except:
            return -1,-1,-1
            

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        result = dict()
        result['id'] = id
        extract_vals = [extractfromdate(x) if x else (numpy.nan,numpy.nan,numpy.nan) for x in input]
        result['extractyear'], result['extractmonth'], result['extractdate'] = map(list, zip(*extract_vals))
        return result
    else:
        result = dict()
        result['id'] = [id]
        extract_vals = [extractfromdate(input) if input else (numpy.nan,numpy.nan,numpy.nan)]
        result['extractyear'], result['extractmonth'], result['extractdate'] = map(list, zip(*extract_vals))
        return result


};