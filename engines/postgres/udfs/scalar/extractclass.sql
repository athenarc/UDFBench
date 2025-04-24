-- U5.	Extractclass: extracts class from string with format funder::class::projectid 

CREATE OR REPLACE FUNCTION extractclass(project text)
    RETURNS text
AS $$
    if project:
        try:
            return project.split("::")[1]
        except:
            return None
    else:
        return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

