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
