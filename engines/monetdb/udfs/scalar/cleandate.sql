-- U3.	Cleandate: Reads a date and converts it to a common format if it is not, handles also dirty dates

CREATE or replace FUNCTION cleandate(input string)
RETURNS STRING
LANGUAGE PYTHON
{
    def cleandate(pubdate):
        if pubdate:
            try:
                if "-" in pubdate:
                    splitnum = pubdate.count('-')
                    pubdate_split = pubdate.split("-")
                    if splitnum ==1:
                        return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                    elif splitnum ==2:
                        return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                    else:
                        return numpy.nan
                elif "/" in pubdate:
                    splitnum = pubdate.count('/')
                    pubdate_split = pubdate.split("/")
                    if splitnum ==1:
                        return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                    elif splitnum ==2:
                        return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                    else:
                        return numpy.nan
                else:
                    return numpy.nan
        
            except:
                return numpy.nan
        else:
            return numpy.nan

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:

        return numpy.array([cleandate(x) if x is not None and x!='-' else numpy.nan for x in input],dtype=object)

    else:
        return numpy.array( [cleandate(input) if input is not None  and input!='-' else numpy.nan],dtype=object)
};
