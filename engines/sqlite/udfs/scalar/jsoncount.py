import json

def jsoncount(jval):
        try:
            if jval[0]=='[':
                tot_json = json.loads(jval)
                return int(len(tot_json))
            else:
                return 1
        except:
            return None

jsoncount.registered = True