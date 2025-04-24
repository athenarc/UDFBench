def extractday(arg):
        try:
            return int(arg[arg.rfind('-')+1:])
        except:
            return -1

extractday.registered = True