

-- U39.	Pivot: Converts rows of a specific attribute (optionally grouped by another attribute) into columns, while applying an aggregation within the transformed dataset. It returns one tuple per input group

CREATE OR REPLACE FUNCTION pivot(
    subquery text, 
    group_by_column text, 
    pivot_column text,    
    aggregate_function text -- Aggregate function to apply(size,sum )
)RETURNS SETOF RECORD
AS $$
    import pandas as pd
    import plpy

    try:
        rows = plpy.execute(subquery)
        data = list(rows)
        df = pd.DataFrame(data)

        pivoted_df = df.pivot_table(
            index=group_by_column,
            columns=pivot_column,
            aggfunc=aggregate_function,
            fill_value=0
        ).reset_index()

        for row in pivoted_df.itertuples(index=False):
            yield tuple(row)

    except:
        return None
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

