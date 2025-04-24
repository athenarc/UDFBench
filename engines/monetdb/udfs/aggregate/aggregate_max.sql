 -- U28. Calculates max date


CREATE OR REPLACE AGGREGATE aggregate_max(val string)
RETURNS string
LANGUAGE PYTHON
{
    if type(val)==numpy.ma.core.MaskedArray:
        val = val.filled(fill_value='')

    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros_like(unique, dtype=val.dtype)
        for i in range(0, unique.size):
            val_i = val[aggr_group==unique[i]]
            val_i = val_i[val_i!='-']
            if val_i.any():
                x[i] = max(val_i)
            else:
                x[i] = numpy.nan
        return (x)
    except NameError:
        val = val[val!='']
        if val.any():
            x = max(val)
        else:
            x = numpy.nan
        return numpy.array([x],dtype=object)
};