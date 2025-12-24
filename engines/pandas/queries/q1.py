import utils

class Q1(utils.PandasQueryBase):
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

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        pd = self.pd
        Artifacts = self.schemas.Artifacts
        data = self.__read_df__(
            dataset_path, 'artifacts',
            [
                Artifacts.id,
                Artifacts.date
            ],
            data_format
        )
        res = pd.concat([
            data[Artifacts.id],
            data[Artifacts.date].apply(self.scalar_udfs.extractday),
            data[Artifacts.date].apply(self.scalar_udfs.extractmonth),
            data[Artifacts.date].apply(self.scalar_udfs.extractyear),
        ], axis=1)
        res.columns = range(res.columns.size)
        return res
