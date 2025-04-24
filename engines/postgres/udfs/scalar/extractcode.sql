-- U6.	Extractcode: Processes a structured string containing the funder’s id, the funding class and the project id, and extracts the project id

CREATE OR REPLACE FUNCTION extractcode(project text)
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
