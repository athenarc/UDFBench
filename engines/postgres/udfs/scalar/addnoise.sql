-- U1.	Addnoise : adds gaussian noise to a value and returns a float

CREATE OR REPLACE FUNCTION addnoise(val NUMERIC)
RETURNS FLOAT
AS $$
    import random

    def add_noise(mean, std_dev, val):
 
        noise = random.gauss(mean, std_dev)
        result = float(val) + noise
        return result
      
    if val:
        return add_noise(0,2,val)
    else:
        return None

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;
