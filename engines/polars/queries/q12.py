import utils
import datetime
import dateutil.relativedelta
import polars as pl

class Q12(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path']
        )

    def __calcT__(self):
        """ Can be overridden by subclasses to change the time window filter. """
        return (
            datetime.datetime.now(datetime.timezone.utc) -
            dateutil.relativedelta.relativedelta(months=18)
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        T = self.__calcT__().strftime('%Y/%m/%d %H:%M:%S')
        print(f'Starting timestamp: {T}')
        return self.__scan_df__(
            dataset_path, 'views_stats', data_format,
            self.schemas.ViewsStats, (
                'date',
                'artifactid',
            ),
        ).map_batches(
            lambda df: (print(f'Initial rows: {len(df):_}') or df)
        ).filter(
            pl.col('date').map_elements(
                lambda d: self.scalar_udfs.cleandate(d) >= T,
                return_dtype=pl.Boolean,
            )
        ).map_batches(
            lambda df: (print(f'Selected rows: {len(df):_}') or df)
        ).group_by('artifactid').len(name='views').select(
            pl.col('artifactid'),
            pl.col('views').map_elements(
                self.scalar_udfs.addnoise,
                return_dtype=pl.Float64,
            ),
        ).sort(by='views', descending=True).limit(10).collect()
