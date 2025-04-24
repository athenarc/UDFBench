

-- U33.	Extractkeys: Selects keys from xml parsed input 

CREATE OR REPLACE FUNCTION extractkeys(jval text,key1 text,key2 text) 
RETURNS TABLE (
    key1 text,
    key2 text
) AS $$
    import json
    import plpy

    try:
        data = json.loads(jval)

        if isinstance(data, list):
            for item in data:
                yield (item.get(key1),item.get(key2))

        elif isinstance(data, dict):
            # Extract values dynamically for all keys in the dictionary
            yield (data.get(key1),data.get(key2))

        else:
            yield (None,None)

    except Exception as e:
        plpy.error(f"Error extracting keys from XML content: {str(e)}")
        return (None,None)
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

