
-- U26.	Avg: Calculates average

CREATE OR REPLACE AGGREGATE aggregate_avg(val INTEGER)
RETURNS float
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = numpy.average(val[aggr_group==unique[i]])
    except NameError:
        x = float(numpy.average(val))
    return (x)
};



CREATE OR REPLACE AGGREGATE aggregate_avg(val numeric)
RETURNS float
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = numpy.average(val[aggr_group==unique[i]])
    except NameError:
        x = float(numpy.average(val))
    return (x)
};