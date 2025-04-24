-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column.

CREATE OR REPLACE FUNCTION getstats( value_column int)
RETURNS TABLE ( avg_val float, median_val float)
LANGUAGE PYTHON
{

    import pandas as pd
    try:
        if type(value_column)==numpy.ndarray or type(value_column)==numpy.ma.core.MaskedArray:
            avg_values=numpy.average(value_column)
            median_values = numpy.ma.median(value_column)

            return pd.DataFrame([(avg_values,median_values)])
        else:

            return pd.DataFrame([(None,None)])

    except:
        return pd.DataFrame([(None,None)])
};

-- U43.	Getstats: gets a whole table with integer values as input and returns the avg and the median for each input column with group by column.

CREATE OR REPLACE FUNCTION getstats(value_column int, group_column string)
RETURNS TABLE (group_column string, avg_val float, median_val float)
LANGUAGE PYTHON {

    import pandas as pd

    def group_avg(group_column, value_column, group_id):
        try:
            group_indices = numpy.where(group_column == group_id)[0]
            group_values = value_column[group_indices]
            avg_value = numpy.average(group_values)
            median_value = numpy.ma.median(group_values)
            return avg_value, median_value
        except:
            return None, None

    try:
        if isinstance(value_column, numpy.ndarray) or isinstance(value_column, numpy.ma.core.MaskedArray):
            unique_groups = numpy.unique(group_column)
            rows = []
            for group_id in unique_groups:
                avg_value, median_value = group_avg(group_column, value_column, group_id)
                rows.append((group_id, avg_value, median_value))
            return pd.DataFrame(rows, columns=['group_column', 'avg_val', 'median_val'])
        else:
            return pd.DataFrame([(None, None, None)], columns=['group_column', 'avg_val', 'median_val'])
    except:
        return pd.DataFrame([(None, None, None)], columns=['group_column', 'avg_val', 'median_val'])
};