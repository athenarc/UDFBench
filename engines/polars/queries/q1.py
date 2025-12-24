import utils
import polars as pl
import polars.datatypes as dt

class Q1(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        return self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, ('id', 'date'),
        ).with_columns(
            pl.col('id'),
            pl.col('date').map_elements(
                self.scalar_udfs.extractday, return_dtype=dt.Int8
            ).alias('day'),
            pl.col('date').map_elements(
                self.scalar_udfs.extractmonth, return_dtype=dt.Int8
            ).alias('month'),
            pl.col('date').map_elements(
                self.scalar_udfs.extractyear, return_dtype=dt.Int16
            ).alias('year'),
        ).collect()
