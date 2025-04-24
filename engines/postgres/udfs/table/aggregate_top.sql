

-- U40.	Top: Processes one group at a time and returns the top N values of an attribute 


CREATE OR REPLACE FUNCTION aggregate_top(subquery text, top_n int,group_col text,value_col text)
RETURNS SETOF record
AS $$
    import pandas as pd

    try:
        rows = plpy.execute(subquery)

        data = list(rows)
        dataset = pd.DataFrame(data) 
        df = dataset.groupby(group_col).apply(lambda x: x.nlargest(top_n, value_col)).reset_index(drop=True)
        df.dropna(inplace=True)  

        for _, row in df.iterrows():
            yield tuple(row.values)

       
    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

