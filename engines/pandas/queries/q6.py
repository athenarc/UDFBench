import utils

class Q6(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
            schema_module,
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        # Works, but converts the modin df returned by udf to pandas df...
        # arxiv = self.pd.Series([self.__create_data_file_path__(
        #     external_data_path, 'arxiv', 'xml'
        # )]).apply(self.table_udfs.file, pd=self.pd, file_type='xml')[0]
        
        arxiv = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(external_data_path, 'arxiv', 'xml'),
            'pd': self.pd,
            'file_type': 'xml'
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0]))
        
        query2json = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(external_data_path, 'query2json', 'txt'),
            'pd': self.pd,
            'file_type': 'json',
            'lines': True,
            'dtype': {col: str for col in ['doi', 'amount', 'totalpubs', 'sdate']}
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0]))

        self.pd.concat(
            [arxiv, query2json],
            ignore_index=True
        ).pipe(
            self.table_udfs.output,
            output_path=self.__gen_output_filename__(
                dir_path=external_data_path,
                df_name='q6',
                data_format='csv',
            ),
            file_type='csv'
        )
        return self.pd.DataFrame()
