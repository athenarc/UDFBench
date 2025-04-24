import pandas as pd
from pyspark.sql.functions import pandas_udf


#  U26.	Avg: Calculates average
@pandas_udf("double")
def aggregate_avg(values: pd.Series) -> float:
    values = pd.to_numeric(values, errors='coerce') 
    values = values.dropna()
    if values.empty:
        return None
    return values.mean()