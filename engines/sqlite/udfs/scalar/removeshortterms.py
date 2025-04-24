import json 

def removeshortterms(jval):

    def removeshortwords(name):
        return " ".join([word for word in name.split(' ') if len(word) > 2])
    try:
        return json.dumps([removeshortwords(name) for name in json.loads(jval)])
    except:
        return "[]"

removeshortterms.registered = True