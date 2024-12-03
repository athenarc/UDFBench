
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





