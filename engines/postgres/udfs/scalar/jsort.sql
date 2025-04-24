-- U19.	Jsort: processes a json list and returns a sorted json list 

CREATE OR REPLACE FUNCTION jsort(jval text)
    RETURNS text
AS $$
    import json

    try:
        return json.dumps(sorted(json.loads(jval)))
    except:
        return "[]"
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
