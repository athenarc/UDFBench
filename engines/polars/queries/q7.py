import utils
import polars as pl

class Q7(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
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
        return pl.LazyFrame(({
            'path': self.__create_data_file_path__(
                external_data_path, 'pubmed_q7.txt'
            ),
            'file_type': 'json',
        },)).map_batches(
            lambda r: self.table_udfs.file(**r.row(0, named=True)),
            schema={
                col: pl.String for col in (
                    'id', 'citations', 'authors',
                )
            }
        ).select((
            pl.col(c)
                .map_elements(
                    self.scalar_udfs.jsoncount,
                    return_dtype=pl.Int64,
                )
                # jsoncount may return None
                # aggregate_avg uses np.isnan, which crashes when checking against None
                .drop_nulls()
                .map_batches(
                    self.aggr_udfs.aggregate_avg,
                    return_dtype=pl.Float64,
                    returns_scalar=True
                )
                .alias(f'avg_{c}')
            for c in ('citations', 'authors')
        )).collect()
