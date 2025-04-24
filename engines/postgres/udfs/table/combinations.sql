

-- U32.	Combinations: Reads a json list and returns a table with all the combinations per an integer parameter

CREATE OR REPLACE FUNCTION combinations(val text,numcomb int)
    RETURNS TABLE  (authorpair text)
AS $$
        import json
        import itertools
        def jcombinations(jval,N):
            try:
                name_list = json.loads(jval)
                for name_per in itertools.combinations(name_list, N):
                    yield [json.dumps(name_i) for name_i in name_per]
    
            except:
                yield('[]')

        for row in jcombinations(val,numcomb):
            yield(row)
$$
LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;