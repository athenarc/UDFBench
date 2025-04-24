
-- U20.	Jsortvalues: processes a json list where each value contains more than one tokens, sorts the tokens in each value 

CREATE OR REPLACE FUNCTION jsortvalues(jval text)
    RETURNS text
AS $$
    import json

    def sortname(name):
        return " ".join(sorted(name.split(' ')))

    try:
        return json.dumps([sortname(name) for name in json.loads(jval)])
    except:
        return "[]"
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;