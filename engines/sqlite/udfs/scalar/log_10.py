import math

def log_10(input):
    try:
        return math.log10(input)
    except:
        return 0.0
log_10.registered = True

