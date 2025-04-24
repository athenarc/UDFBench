-- U23.	Lowerize: Converts to lower case the input text 

CREATE OR REPLACE FUNCTION lowerize(val text)
    RETURNS text
AS $$
    if val:
        try:
            return val.lower()
        except:
            return ''
    else:
        return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;