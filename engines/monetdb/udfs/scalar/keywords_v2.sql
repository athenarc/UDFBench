

-- U21.	Keywords(v2): Removes any punctuation from text, except $numeric, and returns the keywords in one string 

CREATE or replace FUNCTION keywords_v2(input string)
RETURNS string
LANGUAGE PYTHON
{
    import re 
    text_tokens = re.compile(r'([\d.]+\b|\w+|\$[\d.]+)', re.UNICODE)


    def keywords_text(words):
        try:
            res=text_tokens.findall(words)

            return ' '.join((x for x in res if x != '.'))
        except:
            return ''

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([keywords_text(x) if x is not None and x!='-' else numpy.nan for x in input], dtype=object)
    else:
        return numpy.array([keywords_text(input) if input is not None and input!='-' else numpy.nan ], dtype=object)



};