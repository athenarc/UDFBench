import json

def jaccard(input1, input2):
    try:
        r=json.loads(input1)
        s=json.loads(input2)
        rset=set([tuple(x) if type(x)==list else x for x in r])
        sset=set([tuple(x) if type(x)==list else x for x in s])
        return float(len( rset & sset ))/(len( rset | sset ))
    except:
        return 0.0
jaccard.registered = True
