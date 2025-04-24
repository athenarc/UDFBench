-- U22.	Log_10: Calculates and returns the logarithm

CREATE or replace FUNCTION log_10(input float)
RETURNS float
LANGUAGE PYTHON
{
    import math
    def mylog10(x):
        try:
            return math.log10(x)
        except:
            return 0.0

    if type(input)==numpy.ndarray or type(input)==numpy.ma.core.MaskedArray:
        return numpy.array([mylog10(x) if x else None for x in input], dtype=numpy.float64)
    else:
        return numpy.array([mylog10(input) if input else None], dtype=numpy.float64)
};

