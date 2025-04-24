-- U31.	Jsonparse: Parses a json dict per time and returns a tuple with the values

CREATE OR REPLACE FUNCTION jsonparse(subquery text,column_name text,key1  text, key2 text) 
RETURNS SETOF RECORD AS $$
    import plpy

    try:
        import json
        for line in plpy.execute(subquery):
            data = json.loads(line[column_name])
            if isinstance(data, list):
                for item in data:
                    yield (item.get(key1),item.get(key2))
            elif isinstance(data, dict):
                yield (data.get(key1),data.get(key2)) 
            else:
                yield None,None
    

    except Exception as e:
        plpy.error(f"Error parsing JSON content: {str(e)}")
        return None,None


$$ LANGUAGE 'plpython3u'IMMUTABLE STRICT PARALLEL SAFE;
