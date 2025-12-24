import utils

class Q9Bench(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            pd_module,
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
        ArtifactAuthorlists = self.schemas.ArtifactAuthorlists
        authorlists = self.__time_fn__(
            lambda: self.__read_df__(
                dataset_path, 'artifact_authorlists',
                [
                    ArtifactAuthorlists.authorlist,
                ],
                data_format
            ),
            'Read ArtifactAuthorlists'
        )
        jsoncount = self.scalar_udfs.jsoncount
        combinations = self.table_udfs.combinations
        clean = self.scalar_udfs.clean
        
        def json_count_udf(authorList):
            count = jsoncount(authorList)
            return (count is not None) and (count <= 50)
        pairs = self.__time_fn__(
            lambda: authorlists[ArtifactAuthorlists.authorlist][
                authorlists[ArtifactAuthorlists.authorlist].apply(json_count_udf)
            ],
            'json_count_udf'
        )
        
        c = self.__time_fn__(
            lambda: pairs.apply(
                lambda al: combinations(clean(al), 2)
            ),
            'combinations & clean',
        )
        comb = self.__time_fn__(
            lambda: c.explode(ignore_index=True).dropna(),
            'explode and dropna',
        )
        agg_count = self.__time_fn__(
            lambda: comb.pipe(self.aggr_udfs.aggregate_count),
            'aggregate_count',
        )
        return self.__time_fn__(
            lambda: self.pd.DataFrame((agg_count,)),
            'DataFrame',
        )
