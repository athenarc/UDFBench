import utils

class Q18Bench(utils.PandasQueryBase):
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
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        jpack = self.scalar_udfs.jpack
        frequentterms = self.scalar_udfs.frequentterms
        stem = self.scalar_udfs.stem
        filterstopwords = self.scalar_udfs.filterstopwords
        keywords = self.scalar_udfs.keywords

        arxiv = self.__time_fn__(
            lambda: self.pd.DataFrame([{
                'path': self.__create_data_file_path__(external_data_path, 'arxiv', 'csv'),
                'pd': self.pd,
                'file_type': 'csv',
                'header': None
            }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0])),
            'read arxiv'
        )
        arxiv = self.__time_fn__(
            lambda: arxiv.loc[arxiv[1].notna()],
            'filter arxiv nulls'
        )
        arxiv[1] = self.__time_fn__(
            lambda: arxiv[1].apply(
                lambda v: (
                    jpack(frequentterms(
                        stem(filterstopwords(keywords(v))),
                        10
                    ))
                )
            ),
            'arxiv udfs'
        )
        arxiv.columns = ('arxivid', 'arxivterms')
        
        pubmed = self.__time_fn__(
            lambda: self.pd.DataFrame([{
                'path': self.__create_data_file_path__(external_data_path, 'pubmed', 'txt'),
                'pd': self.pd,
                'file_type': 'json',
                'lines': True
            }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0])),
            'read pubmed'
        )
        pubmed = self.__time_fn__(
            lambda: pubmed.loc[pubmed['abstract'].notna()],
            'filter pubmed nulls'
        )
        pubmed['abstract'] = self.__time_fn__(
            lambda: pubmed['abstract'].apply(
                lambda v: (
                    jpack(frequentterms(
                        stem(filterstopwords(keywords(v))),
                        10
                    ))
                )
            ),
            'pubmed udfs'
        )
        pubmed.columns = ('pubmedid', 'pmcterms')

        comb = self.__time_fn__(
            lambda: self.pd.merge(arxiv, pubmed, how='cross'),
            'cross join arxiv and pubmed'
        )
        del arxiv, pubmed

        comb['similarity'] = self.__time_fn__(
            lambda: comb[['arxivterms', 'pmcterms']].apply(
                lambda r: self.scalar_udfs.jaccard(r['arxivterms'], r['pmcterms']),
                axis=1
            ),
            'jaccard similarity'
        )
        del comb['arxivterms'], comb['pmcterms']

        return self.__time_fn__(
            lambda: comb.groupby('arxivid').apply(
                lambda g: self.table_udfs.aggregate_top(g, 5, 'similarity')
            ).reset_index(drop=True).dropna(),
            'aggr_top'
        )
