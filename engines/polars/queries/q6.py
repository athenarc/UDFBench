import utils
import polars as pl

class Q6(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        pl.concat((
            pl.LazyFrame((file_udf_args,)).map_batches(
                lambda r: self.table_udfs.file(**r.row(0, named=True)),
                schema={
                    col: pl.String for col in (
                        'doi', 'amount', 'totalpubs', 'sdate'
                    )
                }
            )
            for file_udf_args in (
                {
                    'path': self.__create_data_file_path__(
                        external_data_path, 'arxiv.xml'
                    ),
                    'file_type': 'xml',
                },
                {
                    'path': self.__create_data_file_path__(
                        external_data_path, 'query2json.txt'
                    ),
                    'file_type': 'json',
                    'lines': True,
                }
            )
        )).collect().pipe(
            self.table_udfs.output,
            output_path=self.__gen_output_filename__(
                dir_path=external_data_path,
                df_name='q6',
                data_format='csv',
            ),
            file_type='csv'
        )
        return pl.DataFrame()
