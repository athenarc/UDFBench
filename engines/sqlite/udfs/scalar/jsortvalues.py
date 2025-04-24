import json 

def jsortvalues(jval):
    def sortname(name):
        return " ".join(sorted(name.split(' ')))

    try:
        return json.dumps([sortname(name) for name in json.loads(jval)])
    except:
        return "[]"
jsortvalues.registered = True
