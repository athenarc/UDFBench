import statistics
import numpy as np

def aggregate_avg(pd_series):
    # return pd_series.mean(skipna=True)
    # return np.nanmean(pd_series)
    try:
        return statistics.mean(
            (i for i in pd_series if not np.isnan(i))
        )
    # statistics.mean throws if generator yields no data
    except statistics.StatisticsError:
        return np.nan

def aggregate_max(itr):
    return max(itr)

def aggregate_median(pd_series):
    # return pd_series.median(skipna=True)
    # return np.nanmedian(pd_series)
    try:
        # we could use np.nanmedian but it does not allow passing a generator
        return statistics.median(
            (i for i in pd_series if not np.isnan(i))
        )
    # statistics.median throws if generator yields no data
    except statistics.StatisticsError:
        return np.nan

def aggregate_count(pd_series):
    return sum(1 for _ in pd_series)
