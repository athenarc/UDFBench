
def lowerize(val):
     if val:
        try:
            return val.lower()
        except:
            return ''
     else:
        return None

lowerize.registered = True