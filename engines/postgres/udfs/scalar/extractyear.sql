
-- U12.  Extractyear : Reads a date (as a string) and extracts an integer with the year

CREATE or replace FUNCTION extractyear(arg text)
    RETURNS INT
AS $$
        if arg:
            try:
                return int(arg[:arg.find('-')])
            except:
                return -1
        else:
            return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
