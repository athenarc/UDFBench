import utils

class Q7(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            aggr_udf_path=udf_paths['aggr_udf_path'],
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        pubmed_q7 = self.table_udfs.file(
            self.__create_data_file_path__(external_data_path, 'pubmed_q7', 'txt'),
            pd=self.pd, file_type='json'
        )

        return self.pd.DataFrame([
            pubmed_q7['citations']
                .apply(self.scalar_udfs.jsoncount)
                .pipe(self.aggr_udfs.aggregate_avg),
            pubmed_q7['authors']
                .apply(self.scalar_udfs.jsoncount)
                .pipe(self.aggr_udfs.aggregate_avg),
        ], ).T
