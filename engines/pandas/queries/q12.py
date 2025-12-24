import utils
import datetime
import dateutil.relativedelta

class Q12(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
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
        ViewsStats = self.schemas.ViewsStats
        data = self.__read_df__(
            dataset_path, 'views_stats',
            [
                ViewsStats.date,
                ViewsStats.artifactid
            ],
            data_format
        )
        T = self.__calcT__().strftime('%Y/%m/%d %H:%M:%S')
        filtered_data = data.loc[
            data[ViewsStats.date].apply(
                lambda d: self.scalar_udfs.cleandate(d) >= T
            )
        ]
        print(f'Initial rows: {len(data):_}')
        print(f'Starting timestamp: {T}')
        print(f'Selected rows: {len(filtered_data):_}')
        res = filtered_data.groupby(
            [ViewsStats.artifactid]
        ).size().reset_index(name='views')
        res['views'] = res['views'].apply(self.scalar_udfs.addnoise)
        return res.sort_values(by='views', ascending=False)[:10]
