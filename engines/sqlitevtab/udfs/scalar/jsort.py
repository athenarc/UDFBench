import json 

def jsort(jval):
    try:
        return json.dumps(sorted(json.loads(jval)))
    except:
        return "[]"

jsort.registered=True
