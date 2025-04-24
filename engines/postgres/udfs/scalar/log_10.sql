

-- U22.	Log_10: Calculates and returns the logarithm

CREATE OR REPLACE FUNCTION log_10(input numeric)
    RETURNS double precision
AS $$
    import math
    try:
        return math.log10(input)
    except:
        return 0.0

$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;