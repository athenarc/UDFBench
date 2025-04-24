

-- U8.	Extractfunder: extracts funder from string with format funder::class::projectid

CREATE OR REPLACE FUNCTION extractfunder(project text)
    RETURNS text
AS $$
    if project:
        try:
            if '::' in project:
                return project.split("::")[0]
            else:
                return None
        except:
            return None
    else:
        return None
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
