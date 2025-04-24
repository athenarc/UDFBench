def extractmonth(arg):
        try:
            return int(arg[arg.find('-')+1:arg.rfind('-')])
        except:
            return -1

extractmonth.registered = True
