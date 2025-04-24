-- U7.	Extractday: Reads a date (as a string) and extracts an integer with the day 

CREATE or replace FUNCTION extractday(arg text)
    RETURNS INT
AS $$
        if arg:
            try:
                return int(arg[arg.rfind('-')+1:])
            except:
                return -1
        else:
            return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
