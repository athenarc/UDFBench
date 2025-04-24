import pandas as pd
from pyspark.sql.functions import pandas_udf


#  U29.	Median: Calculates median
@pandas_udf("double")
def aggregate_median(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors='coerce') 
    values = values.dropna()
    if values.empty:
        return None
    return values.median()
