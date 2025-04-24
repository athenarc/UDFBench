-- U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

CREATE OR REPLACE FUNCTION strsplitv(input STRING)
RETURNS TABLE  (word STRING)
LANGUAGE PYTHON
{
    def strsplitv(val):
        try:
            return val.split()   
        except:
            return []

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        res = numpy.array([y if arg and arg!='-' else numpy.nan for arg in input for y in strsplitv(arg)], dtype=object)
    else:
        res =  numpy.array([y for y in strsplitv(input)], dtype=object)

    if not res.any():
        return ['[]']
    else:
        return res

};



-- U34.	Strsplitv(q17): Processes a string at a time and returns its tokens in separate rows 



CREATE OR REPLACE FUNCTION strsplitv(docid string, abstract string) 
RETURNS TABLE (docid string, term string) 
LANGUAGE PYTHON
{
    import pandas as pd
    def strsplitv(val):
        try:
            return val.split()   
        except:
            return [""]

    if type(docid)==numpy.ndarray or type(docid)==numpy.ma.core.MaskedArray:

        res=  pd.DataFrame([[id,y] for id,arg in zip(docid,abstract)  if arg and arg!='-' for y in strsplitv(arg) ], columns=['docid', 'term'])
    else:
        res = pd.DataFrame([[docid,y] for y in strsplitv(abstract) ], columns=['docid', 'term'])
    
    if not res.empty:
        return res
    else:
        return pd.DataFrame({'docid': [], 'term': []})

};