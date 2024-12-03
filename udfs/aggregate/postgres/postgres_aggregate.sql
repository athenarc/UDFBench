

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


-- U27.	Count: Calculates count 


CREATE OR REPLACE FUNCTION aggr_count_final(state numeric[])
RETURNS integer
LANGUAGE plpython3u
AS $$
    return len(state)
$$ IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_count(value numeric) (
    SFUNC = array_append,
    STYPE = numeric[],
    FINALFUNC = aggr_count_final,
    PARALLEL = SAFE


);

CREATE OR REPLACE FUNCTION aggregate_count_step(state bigint, value text) RETURNS bigint AS $$
  global state
  if state is None:
      state = 0
  return state + 1
$$ LANGUAGE plpython3u IMMUTABLE STRICT PARALLEL SAFE;


CREATE  FUNCTION aggr_count_final(state bigint) RETURNS bigint AS $$
  return state
$$ LANGUAGE plpython3u IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_count(text) (
  SFUNC = aggregate_count_step,
  STYPE = bigint,
  FINALFUNC = aggr_count_final,
  INITCOND = '0',
  PARALLEL = SAFE 

);


-- U27.	Count: Calculates count (v2)

--- memory limitation /  faster
CREATE FUNCTION aggr_count_final(state text[])
RETURNS integer
LANGUAGE plpython3u
AS $$
    return len(state)
$$ IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_count_v2(value text) (
    SFUNC = array_append,
    STYPE = text[],
    FINALFUNC = aggr_count_final,
    PARALLEL = SAFE


);



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

--U40. Aggregate top (v2)

CREATE TYPE topn_item AS (
    value numeric,
    id text
);

CREATE OR REPLACE FUNCTION topn_step(state topn_item[], value numeric, id text, n integer)
RETURNS topn_item[]
LANGUAGE plpython3u
AS $$
    import plpy
    if state is None:
        return [(value, id)]
    else:
        state.append({'value': value, 'id': id})
        state.sort(key=lambda x: x['value'], reverse=True)
        return [(item['value'], item['id']) for item in state[:n]]
$$ IMMUTABLE STRICT PARALLEL SAFE;


CREATE OR REPLACE FUNCTION topn_final(state topn_item[])
RETURNS topn_item[]
LANGUAGE plpython3u
AS $$
    return state
$$ IMMUTABLE STRICT PARALLEL SAFE;

CREATE AGGREGATE aggregate_top_v2(numeric, text, integer) (
    SFUNC = topn_step,
    STYPE = topn_item[],
    FINALFUNC = topn_final,
    INITCOND = '{}',
    PARALLEL = SAFE
);
