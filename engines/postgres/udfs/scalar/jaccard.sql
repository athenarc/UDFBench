

-- U15.	Jaccard: Processes two json lists with tokens and calculated the jaccard distance

CREATE or replace FUNCTION jaccard(input1 text, input2 text)
    RETURNS double precision
AS $$

    import json 

    
    try:
        r=json.loads(input1)
        s=json.loads(input2)
        rset=set([tuple(x) if type(x)==list else x for x in r])
        sset=set([tuple(x) if type(x)==list else x for x in s])
        return float(len( rset & sset ))/(len( rset | sset ))
    except:
        return None

            
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


