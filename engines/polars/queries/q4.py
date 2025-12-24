import utils
import polars as pl

class Q4(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            schema_module,
            aggr_udf_path=udf_paths['aggr_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        return self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, ('authors',),
        ).select(
            pl.col('authors').map_batches(
                self.aggr_udfs.aggregate_avg,
                return_dtype=pl.Float64,
                returns_scalar=True,
            ).alias('avg'),
            pl.col('authors').map_batches(
                self.aggr_udfs.aggregate_median,
                return_dtype=pl.Float64,
                returns_scalar=True,
            ).alias('median')
        ).collect()
