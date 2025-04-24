import pandas as pd
from pyspark.sql.functions import pandas_udf

#  U28. Max: Calculates max date with group by

@pandas_udf("string")
def aggregate_max(values: pd.Series) -> float:
    values = values.dropna()
    return values.max()
