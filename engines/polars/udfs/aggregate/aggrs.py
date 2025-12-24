import statistics
import polars as pl
import numpy as np
from typing import Iterable
from numbers import Number

def aggregate_avg(series: pl.Series):
    try:
        return float(statistics.mean(
            # Crashes if i is None
            (i for i in series if not np.isnan(i))
        ))
    # statistics.mean throws if generator yields no data
    except statistics.StatisticsError:
        return 

def aggregate_max(itr: Iterable[Number]):
    return max(itr)

def aggregate_median(series: pl.Series):
    try:
        return float(statistics.median(
            (i for i in series if not np.isnan(i))
        ))
    # statistics.median throws if generator yields no data
    except statistics.StatisticsError:
        return np.nan

def aggregate_count(series: pl.Series):
    return sum(1 for _ in series)
