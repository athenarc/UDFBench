import utils

class Q13(utils.PandasQueryBase):
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
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        crossref = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(external_data_path, 'crossref', 'txt'),
            'pd': self.pd, 
            'file_type': 'txt'
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0]))

        df = crossref.pipe(
            self.table_udfs.jsonparse,
            self.pd,
            'publicationdoi',
            'fundinginfo'
        )
        
        df['projectid'] = df['fundinginfo'].apply(
            self.scalar_udfs.extractprojectid
        )
        return df[['publicationdoi', 'projectid']]
