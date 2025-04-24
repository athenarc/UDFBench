import json
def jsonparse_q14(json_content, key):
  try:

    data = json.loads(json_content)
    
    if isinstance(data, list):
        for item in data:
            return item.get(key)
    if isinstance(data, dict):
        return data.get(key)
    else:
        return None
  except Exception as e:
    return None


jsonparse_q14.registered = True