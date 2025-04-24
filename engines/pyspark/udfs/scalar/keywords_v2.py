
import re

# U21.	Keywords(v2): Removes any punctuation from text, except $numeric, and returns the keywords in one string 

def keywords_v2(input:str)->str:
    import re

    text_tokens = re.compile(r'([\d.]+\b|\w+|\$[\d.]+)', re.UNICODE)

    if input:
        try:
            res=text_tokens.findall(input)

            return ' '.join((x for x in res if x != '.' ))
        except:
            return ''
    else:
        return None