
-- U35.	JGROUPORDERED: Processes a subquery which is ordered by an attribute, and runs a group by with an aggregate defined as a (named) parameter

CREATE OR REPLACE FUNCTION JGROUPORDERED(
    subquery text,
    order_by_col text,
    count_col text
)
RETURNS TABLE ( term text,docid text, tf float, jcount bigint)
AS $$
    import pandas as pd

    def process_ordered_group(subquery, order_by_col,count_col):
        try:
            rows = plpy.execute(subquery + f" ORDER BY {order_by_col}")
            data = list(rows)

            df = pd.DataFrame(data)

            df['jcount'] = df.groupby([order_by_col])[count_col].transform('size')

            for _, row in df.iterrows():
                yield tuple(row.values)

        except Exception as e:
            plpy.error(f"Error processing ordered group: {str(e)}")
            return None

    return process_ordered_group(subquery, order_by_col,count_col)
$$ LANGUAGE 'plpython3u' IMMUTABLE STRICT PARALLEL SAFE;

