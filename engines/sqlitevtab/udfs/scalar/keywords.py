
import  re

text_tokens = re.compile(r'([\d.]+\b|\w+)', re.UNICODE)

def keywords(input):
    if input:
        try:
            res=text_tokens.findall(input)
            return ' '.join((x for x in res if x != '.' ))
        except:
            return ''
    else:
        return None


keywords.registered=True