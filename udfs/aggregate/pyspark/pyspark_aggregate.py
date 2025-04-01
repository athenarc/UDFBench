import pandas as pd
from pyspark.sql.functions import pandas_udf, PandasUDFType



# class Aggregate:

#  U26.	Avg: Calculates average
@pandas_udf("double", PandasUDFType.GROUPED_AGG)
def aggregate_avg(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors='coerce') 
    values = values.dropna()
    if values.empty:
        return None
    return values.mean()

#  U27.	Count: Calculates count 
@pandas_udf("long", PandasUDFType.GROUPED_AGG)
def aggregate_count(values: pd.Series) -> int:
    return values.count()


#  U28. Max: Calculates max date with group by

@pandas_udf("string", PandasUDFType.GROUPED_AGG)
def aggregate_max(values: pd.Series) -> float:
    values = values.dropna()
    return values.max()

#  U29.	Median: Calculates median
@pandas_udf("double", PandasUDFType.GROUPED_AGG)
def aggregate_median(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors='coerce') 
    values = values.dropna()
    if values.empty:
        return None
    return values.median()
