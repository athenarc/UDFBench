
-- U18.	Jsonparse: Parses a json dict per time and returns a string with the value

CREATE OR REPLACE FUNCTION jsonparse(json_content text,key1 text) RETURNS text AS $$
    import plpy
    import json

    try:

        data = json.loads(json_content)
        if isinstance(data, list):
            for item in data:
                return item.get(key1)
        elif isinstance(data, dict):
             return data.get(key1)
        else:
            return None

    except Exception as e:
        plpy.error(f"Error parsing JSON content: {str(e)}")
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
