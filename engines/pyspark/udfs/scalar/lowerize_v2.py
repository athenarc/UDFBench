
import json

# U23.	Lowerize(v2): processes a json list and returns a lower json list

def lowerize_v2(jval: str)->str:
    if jval:
        try:
            return json.dumps([name.lower() for name in json.loads(jval)])
        except:
            return  "[]"
    else:
        return None