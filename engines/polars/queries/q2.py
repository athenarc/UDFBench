import utils
import polars as pl

class Q2(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths
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
        return self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, ('id', 'date'),
        ).with_columns(
            pl.col('id'),
            pl.col('date').map_elements(
                self.table_udfs.extractfromdate,
                return_dtype=pl.List(pl.Int16)
            ).list.to_struct(fields=('year', 'month', 'day'))
        ).unnest("date").collect()
