-- U16.	Jpack: Converts a string to a json list with tokens

CREATE or replace FUNCTION jpack(input text)
    RETURNS text
AS $$
    import json 

    if input:

        try:
            string_split = input.split()
            return json.dumps([word for word in string_split])
        except:
            return ''
    else:
        return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
