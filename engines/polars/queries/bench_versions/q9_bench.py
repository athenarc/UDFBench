import utils
import polars as pl

class Q9Bench(utils.PolarsQueryBase):
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
        
        aa = self.__time_fn__(
            lambda: self.__scan_df__(
                dataset_path, 'artifact_authorlists', data_format,
                self.schemas.ArtifactAuthorlists, (
                    'authorlist',
                ),
            ).collect(),
            'Read ArtifactAuthorlists'
        ).lazy()
        f = self.__time_fn__(
            lambda: aa.filter(
                pl.col('authorlist').map_elements(
                    json_count_wrapper,
                    return_dtype=pl.Boolean,
                )
            ).collect(),
            'json_count_wrapper'
        ).lazy()
        comb = self.__time_fn__(
            lambda: f.select(
                pl.col('authorlist').map_elements(
                    lambda al: self.table_udfs.combinations(
                        self.scalar_udfs.clean(al), 2
                    ),
                    return_dtype=pl.List(pl.String),
                ).explode().drop_nulls()
            ).collect(),
            'combinations and explode'
        ).lazy()

        return self.__time_fn__(
            lambda: comb.select(
                pl.col('authorlist').map_batches(
                    self.aggr_udfs.aggregate_count,
                    return_dtype=pl.Int64,
                    returns_scalar=True,
                )
            ).collect(),
            'aggregate_count'
        )
