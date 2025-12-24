import utils

class Q5Bench(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):        
        a = self.__time_fn__(
            lambda: self.__scan_df__(
                dataset_path, 'artifacts', data_format,
                self.schemas.Artifacts, ('authors',),
            ).collect(),
            'Read Artifacts authors'
        ).lazy()
        
        return self.__time_fn__(
            lambda: a.pipe(self.table_udfs.get_stats).collect(),
            'getstats'
        )
