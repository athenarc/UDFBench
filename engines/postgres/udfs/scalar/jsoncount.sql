-- U17.	Jsoncount: Returns the length of a json list

CREATE or replace FUNCTION jsoncount(jval text)
    RETURNS INT
AS $$
        import json
        try:
            if jval[0]=='[':
                tot_json = json.loads(jval)
                return int(len(tot_json))
            else:
                return 1
        except:
            return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;