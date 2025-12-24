import utils

class Q4(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            pd_module,
            schema_module,
            aggr_udf_path=udf_paths['aggr_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        Artifacts = self.schemas.Artifacts
        artifacts = self.__read_df__(
            dataset_path, 'artifacts',
            [
                Artifacts.authors,
            ],
            data_format
        )
        return self.pd.DataFrame(((
            artifacts[Artifacts.authors].pipe(self.aggr_udfs.aggregate_avg),
            artifacts[Artifacts.authors].pipe(self.aggr_udfs.aggregate_median)
        ),))
