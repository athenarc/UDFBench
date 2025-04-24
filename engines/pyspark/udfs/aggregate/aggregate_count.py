import pandas as pd
from pyspark.sql.functions import pandas_udf



#  U27.	Count: Calculates count 
@pandas_udf("long")
def aggregate_count(values: pd.Series) -> int:
    return values.count()
