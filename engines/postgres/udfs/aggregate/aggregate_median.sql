-- U29.	Median: Calculates median


CREATE OR REPLACE FUNCTION aggr_median_final(state numeric[])
RETURNS numeric
LANGUAGE plpython3u
AS $$
    sorted_values = sorted(state)
    n = len(sorted_values)

    if n % 2 == 0:
        mid = n // 2
        return float(sorted_values[mid - 1] + sorted_values[mid]) / 2.0
    else:
        return sorted_values[n // 2]

$$ IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_median(value numeric) (
    SFUNC = array_append,
    STYPE = numeric[],
    FINALFUNC = aggr_median_final,
    INITCOND='{}',
    PARALLEL = SAFE


);