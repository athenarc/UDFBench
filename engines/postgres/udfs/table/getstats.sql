

-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

CREATE OR REPLACE FUNCTION getstats(subquery text, value_column text,group_column text)
RETURNS SETOF record
AS $$
    import numpy as np
    import plpy

    def group_avg_median(group_column, value_column, group_id):
        try:
            group_indices = np.where(group_column == group_id)[0]

            group_values = value_column[group_indices]
            avg_indices = np.nanmean(group_values)
            median_indices = np.ma.median(group_values)
            return avg_indices,median_indices

        except Exception as e:
            plpy.error(f"Error processing group {group_id}: {str(e)}")
            return None

    try:
        rows = plpy.execute(subquery)
        if group_column:
            value_column_np = np.array([row[value_column] for row in rows])  
            group_column_np = np.array([row[group_column] for row in rows]) 

            unique_groups = list(set(group_column_np))

            for group_id in unique_groups:
                avg_values,median_values= group_avg_median(group_column_np, value_column_np, group_id)
                yield (group_id,float(avg_values),float(median_values))

        else:
            value_column_np = np.array([row[value_column] for row in rows]) 
            value_column_np = value_column_np[value_column_np !=None]
            avg_values=np.average(value_column_np)

            median_values = np.ma.median(value_column_np)

            yield float(avg_values),float(median_values)
       
    except Exception as e:
        plpy.error(f"Error returning stats: {str(e)}")
        yield None
$$
LANGUAGE 'plpython3u';