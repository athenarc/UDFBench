
def extractyear(arg):
        try:
            return int(arg[:arg.find('-')])
        except:
            return -1

extractyear.registered = True