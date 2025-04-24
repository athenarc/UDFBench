
-- U11.	Extractprojectid: Processes a text snippet and extracts a 6 digit project identifier 

CREATE OR REPLACE FUNCTION extractprojectid(input text)
    RETURNS text
AS $$

    import re
    if input:
        try:
            return re.findall(r"(?<!\d)[0-9]{6}(?!\d)",input)[0]
        except: return ''
    else:
        return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;