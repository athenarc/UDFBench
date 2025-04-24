-- U15.	Jaccard: Processes two json lists with tokens and calculated the jaccard distance

CREATE or replace FUNCTION jaccard(input1 string,input2 string)
RETURNS float
LANGUAGE PYTHON
{
    import json 

    def jaccard_text(arg1,arg2):
        try:
            r=json.loads(arg1)
            s=json.loads(arg2)
            rset=set([tuple(x) if type(x)==list else x for x in r])
            sset=set([tuple(x) if type(x)==list else x for x in s])
            return float(len( rset & sset ))/(len( rset | sset ))
        except:
            return None

    if type(input1)==numpy.ndarray or type(input1)==numpy.ma.core.MaskedArray:
        return numpy.array([jaccard_text(arg1,arg2)  if (arg1 is not None and arg1!='-') and (arg2 is not None and arg2!='-') else None for arg1,arg2 in zip(input1,input2)], dtype=numpy.float64)
    else:
        return numpy.array([jaccard_text(input1,input2)  if (input1 is not None and input1!='-') and (input2 is not None and input2!='-') else None ], dtype=numpy.float64)


};
