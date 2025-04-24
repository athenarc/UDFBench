
 -- U28. Calculates max date

CREATE OR REPLACE FUNCTION aggr_max_final(state text[])
RETURNS text
LANGUAGE plpython3u
AS $$
    
    return max(filter(None.__ne__, state),default=None)


$$ IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_max(value text) (
    SFUNC = array_append,
    STYPE = text[],
    FINALFUNC = aggr_max_final,
    PARALLEL = SAFE


);
