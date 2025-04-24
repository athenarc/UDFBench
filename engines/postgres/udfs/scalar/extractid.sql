-- U9.	Extractid: extracts project id from string with format funder::class::projectid 

CREATE OR REPLACE FUNCTION extractid(project text)
    RETURNS text
AS $$
    if project:
        try:
            return project.split("::")[2]
        except:
            return None
    else:
        return None
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
