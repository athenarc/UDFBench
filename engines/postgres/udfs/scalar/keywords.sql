
-- U21.	Keywords: Removes any punctuation from text and returns the keywords in one string 

CREATE or replace FUNCTION keywords(input text)
    RETURNS text
AS $$
    import re 
    text_tokens = re.compile(r'([\d.]+\b|\w+)', re.UNICODE)

    if input:
        try:
            res=text_tokens.findall(input)

            return ' '.join((x for x in res if x != '.' ))
        except:
            return ''
    else:
        return None

            
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;