import utils
import polars as pl

class Q9(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            aggr_udf_path=udf_paths['aggr_udf_path'],
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        def json_count_wrapper(authorList):
            count = self.scalar_udfs.jsoncount(authorList)
            return (count is not None) and (count <= 50)
        
        return self.__scan_df__(
            dataset_path, 'artifact_authorlists', data_format,
            self.schemas.ArtifactAuthorlists, (
                'authorlist',
            ),
        ).filter(
            pl.col('authorlist').map_elements(
                json_count_wrapper,
                return_dtype=pl.Boolean,
            )
        ).select(
            pl.col('authorlist').map_elements(
                lambda al: self.table_udfs.combinations(
                    self.scalar_udfs.clean(al), 2
                ),
                return_dtype=pl.List(pl.String),
            ).explode().drop_nulls().map_batches(
                self.aggr_udfs.aggregate_count,
                return_dtype=pl.Int64,
                returns_scalar=True,
            )
        ).collect()
