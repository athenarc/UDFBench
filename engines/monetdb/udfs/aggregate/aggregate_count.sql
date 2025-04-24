-- U27.	Count: Calculates count 

CREATE OR REPLACE AGGREGATE aggregate_count(val INTEGER)
RETURNS int
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = len(val[aggr_group==unique[i]])
    except NameError:
        x = val.size
    return (x)
};

CREATE OR REPLACE AGGREGATE aggregate_count(val numeric)
RETURNS int
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = len(val[aggr_group==unique[i]])
    except NameError:
        x = val.size
    return (x)
};


CREATE OR REPLACE AGGREGATE aggregate_count(val string)
RETURNS int
LANGUAGE PYTHON
{
    try:
        unique = numpy.unique(aggr_group)
        x = numpy.zeros(shape=(unique.size))

        for i in range(0, unique.size):
            x[i] = len(val[aggr_group==unique[i]])
    except NameError:
        x = val.size
    return (x)
};


