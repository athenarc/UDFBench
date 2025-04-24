
-- U10. Extractmonth: Reads a date (as a string) and extracts an integer with the month


CREATE or replace FUNCTION extractmonth(arg text)
    RETURNS INT
AS $$
        if arg:
            try:
                return int(arg[arg.find('-')+1:arg.rfind('-')])
            except:
                return -1
        else:
            return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
