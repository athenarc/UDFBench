import utils
import polars as pl

class Q13(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        return pl.LazyFrame(({
            'path': self.__create_data_file_path__(
                external_data_path, 'crossref.txt'
            ),
            'file_type': 'txt'
        },)).map_batches(
            lambda r: self.table_udfs.file(**r.row(0, named=True)),
            schema={'text': pl.String}
        ).map_batches(
            lambda df: self.table_udfs.jsonparse(
                df,
                'publicationdoi',
                'fundinginfo'
            ),
            schema={
                'publicationdoi': pl.String,
                'fundinginfo': pl.String
            }
        ).select(
            pl.col('publicationdoi'),
            pl.col('fundinginfo').map_elements(
                self.scalar_udfs.extractprojectid,
                return_dtype=pl.String,
            ).alias('projectid')
        ).collect()
