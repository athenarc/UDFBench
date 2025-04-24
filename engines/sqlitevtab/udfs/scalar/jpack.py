import json

def jpack(input):
    if input:

        try:
            string_split = input.split()
            return json.dumps([word for word in string_split])
        except:
            return ''
    else:
        return None

jpack.registered = True

