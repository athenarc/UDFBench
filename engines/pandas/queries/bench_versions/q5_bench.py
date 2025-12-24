import utils

class Q5Bench(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
            schema_module,
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):            
        get_stats = self.table_udfs.get_stats
        Artifacts = self.schemas.Artifacts
        
        a = self.__time_fn__(
            lambda: self.__read_df__(
                dataset_path, 'artifacts',
                [Artifacts.authors],
                data_format
            ),
            'Read Artifacts authors'
        )
        return self.__time_fn__(
            lambda: a.pipe(get_stats, self.pd.DataFrame),
            'getstats'
        )
