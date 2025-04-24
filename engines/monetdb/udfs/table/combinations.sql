
-- U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter
CREATE or replace FUNCTION combinations(input1 string, input2 integer)
RETURNS TABLE  (authorpair string)
LANGUAGE PYTHON
{

    import json
    import itertools
    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            res = numpy.array([y for arg1,arg2 in zip(input1,input2) for y in jcombinations(arg1,arg2)], dtype=object)
            if not res.any():
                return ['[]']
            else:
                return res

        else:
            res =  numpy.array([y for y in jcombinations(input1,input2)], dtype=object)
            if not res.any():
                return ['[]']
            else:
                return res

    except:
        return ['[]']

};

-- U32.	Combinations(for q16): Reads a json list and returns a table with all the combinations per an integer parameter



CREATE or replace FUNCTION combinations(pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string, input1 string, input2 integer)
RETURNS TABLE  (pubid string, pubdate string, projectstart string, projectend string, funder string, fclass string, projectid string,authorpair string)
LANGUAGE PYTHON
{

    import json
    import itertools
    import pandas as pd


    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            reslist = {
                'pubid': [],
                'pubdate': [],
                'projectstart': [],
                'projectend': [],
                'funder': [],
                'fclass': [],
                'projectid': [],
                'authorpair': []
            }
            for _pubid, _pubdate, _projectstart, _projectend,_funder,_class,_projectid,arg1,arg2 in zip(pubid, pubdate, projectstart, projectend,funder,fclass,projectid,input1,input2):
                _pubdate = _pubdate if _pubdate and _pubdate!='-' else numpy.nan
                _projectstart = _projectstart if _projectstart and _projectstart!='-' else numpy.nan
                _projectend = _projectend if _projectend!='-' else numpy.nan
                for y in jcombinations(arg1,arg2):
                    reslist['pubid'].append(_pubid)
                    reslist['pubdate'].append(_pubdate)
                    reslist['projectstart'].append(_projectstart)
                    reslist['projectend'].append(_projectend)
                    reslist['funder'].append(_funder)
                    reslist['fclass'].append(_class)
                    reslist['projectid'].append(_projectid)
                    reslist['authorpair'].append(y)

            return pd.DataFrame(reslist)
        else:
            res = pd.DataFrame([[pubid, pubdate, projectstart, projectend,funder,fclass,projectid,y] for y in jcombinations(input1,input2)])
        
        if not res.empty:
            return res
        else:
            return pd.DataFrame({'pubid': [], 'pubdate': [], 'projectstart': [], 'projectend': [], 'funder': [], 'fclass': [], 'projectid': [], 'authorpair': []})

    except:
        return pd.DataFrame({'pubid': [], 'pubdate': [], 'projectstart': [], 'projectend': [], 'funder': [], 'fclass': [], 'projectid': [], 'authorpair': []})

};

-- U32.	Combinations(for q10a and q11a): Reads a json list and returns a table with all the combinations per an integer parameter


CREATE or replace FUNCTION combinations(pubdate STRING, input1 STRING, input2 INTEGER)
RETURNS TABLE  (authorpair STRING, pubdate STRING)
LANGUAGE PYTHON
{

    import json
    import itertools
    import pandas as pd
    def jcombinations(jval,N):
        try:
            name_list = json.loads(jval)
            for name_per in itertools.combinations(name_list, N):
                yield json.dumps([name_per_i for name_per_i in name_per])

        except:
            yield('[]')  
    try:
        if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
            reslist = {
                'authorpair': [],
                'pubdate': []

            }
            for _pubdate, arg1,arg2 in zip(pubdate, input1,input2):
                _pubdate = _pubdate if _pubdate and _pubdate!='-' else numpy.nan
                for y in jcombinations(arg1,arg2):
                    reslist['pubdate'].append(_pubdate)
                    reslist['authorpair'].append(y)

            return pd.DataFrame(reslist)
        else:
            res = pd.DataFrame([[ pubdate,y] for y in jcombinations(input1,input2)])
        
        if not res.empty:
            return res
        else:
            return pd.DataFrame({ 'pubdate': [], 'authorpair': []})

    except:
        return pd.DataFrame({ 'pubdate': [], 'authorpair': []})

};
