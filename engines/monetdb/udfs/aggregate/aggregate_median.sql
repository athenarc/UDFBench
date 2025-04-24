-- U29.	Median: Calculates median

CREATE OR REPLACE AGGREGATE aggregate_median(val INTEGER)
RETURNS float
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = numpy.ma.median(val[aggr_group==unique[i]])
    except NameError:
        x = numpy.ma.median(val)
    return (x)
};

CREATE OR REPLACE AGGREGATE aggregate_median(val numeric)
RETURNS float
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = numpy.ma.median(val[aggr_group==unique[i]])
    except NameError:
        x = numpy.ma.median(val)
    return (x)
};





