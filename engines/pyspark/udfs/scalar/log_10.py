import math

# U22.	Log_10: Calculates and returns the logarithm

def log_10(x:float)->float:
    try:
        return math.log10(x)
    except:
        return 0.0
