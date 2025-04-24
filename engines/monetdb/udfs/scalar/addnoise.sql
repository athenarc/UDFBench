-- U1. Add_noise : adds gaussian noise to a value and returns a float 

CREATE OR REPLACE FUNCTION addnoise(val float)
RETURNS float
LANGUAGE PYTHON
{   import random

    def add_noise(val, mean=0, std_dev=2):
        try:
            noise = random.gauss(mean, std_dev)
            result = float(val) + noise
            return result

        except:
            return -1
    

    if type(val)==numpy.ndarray or type(val)==numpy.ma.core.MaskedArray:
        return numpy.ma.array([add_noise(x) if x else None for x in val], dtype=numpy.float64)
    else:
        return numpy.ma.array([add_noise(val)] if val else None, dtype=numpy.float64)


};
