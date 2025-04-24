

-- U26.	Avg: Calculates average


CREATE OR REPLACE FUNCTION float8_avg(arr float8[])
RETURNS float8 AS $$
    if arr[0] == 0:
        return None
    return arr[1] / arr[0]
$$ LANGUAGE plpython3u IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_avg (float8)
(
    sfunc = float8_accum,
    stype = float8[],
    finalfunc = float8_avg,
    initcond = '{0,0,0}',
    PARALLEL = SAFE
);

