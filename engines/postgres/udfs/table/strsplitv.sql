

-- U34.	Strsplitv: Processes a string at a time and returns its tokens in separate rows 

CREATE OR REPLACE FUNCTION strsplitv(val text)
    RETURNS TABLE  (word text)
AS $$

        def strsplitv(val):
            try:
                return val.split()   
            except:
                return ['']
        return strsplitv(val)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;


