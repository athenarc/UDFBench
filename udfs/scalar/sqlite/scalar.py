import json
import random

def cleandate(pubdate):
    if pubdate:
        try:
            if "-" in pubdate:
                splitnum = pubdate.count('-')
                pubdate_split = pubdate.split("-")
                if splitnum ==1:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                elif splitnum ==2:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + pubdate_split[2]
                else:
                    return None
            elif "/" in pubdate:
                splitnum = pubdate.count('/')
                pubdate_split = pubdate.split("/")
                if splitnum ==1:
                    return pubdate_split[0] + "/" + pubdate_split[1] + "/" + "01"
                elif splitnum ==2:
                    return pubdate_split[0] + "-" + pubdate_split[1] + "-" + pubdate_split[2]
                else:
                    return None
            else:
                return None
        except:
            return None
    else:
        return None
cleandate.registered = True

def add_noise(val):

    def add_noise(mean, std_dev, val):

        noise = random.gauss(mean, std_dev)
        result = val + noise
        return result


    return add_noise(0,2,val)

add_noise.registered = True


def jsonparse(json_content, key):
  try:

    # Parse the JSON string
    data = json.loads(json_content)
    
    if isinstance(data, list):
        for item in data:
            return item.get(key)
    # Check if the input is a dictionary
    elif isinstance(data, dict):
        # Extract values dynamically for all keys in the dictionary
        return data.get(key)
    else:
        return None
  except Exception as e:
    return None


jsonparse.registered = True


def extractyear(arg):
        try:
            return int(arg[:arg.find('-')])
        except:
            return -1

extractyear.registered = True


def extractmonth(arg):
        try:
            return int(arg[arg.find('-')+1:arg.rfind('-')])
        except:
            return -1

extractmonth.registered = True


def extractday(arg):
        try:
            return int(arg[arg.rfind('-')+1:])
        except:
            return -1

extractday.registered = True

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



