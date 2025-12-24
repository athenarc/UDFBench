import utils

class Q18(utils.PandasQueryBase):
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

        arxiv = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(external_data_path, 'arxiv', 'csv'),
            'pd': self.pd,
            'file_type': 'csv',
            'header': None
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0]))
        arxiv = arxiv.loc[arxiv[1].notna()]
        arxiv[1] = arxiv[1].apply(
            lambda v: (
                jpack(frequentterms(
                    stem(filterstopwords(keywords(v))),
                    10
                ))
            )
        )
        arxiv.columns = ('arxivid', 'arxivterms')
        
        pubmed = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(external_data_path, 'pubmed', 'txt'),
            'pd': self.pd,
            'file_type': 'json',
            'lines': True
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0]))
        pubmed = pubmed.loc[pubmed['abstract'].notna()]
        pubmed['abstract'] = pubmed['abstract'].apply(
            lambda v: (
                jpack(frequentterms(
                    stem(filterstopwords(keywords(v))),
                    10
                ))
            )
        )
        pubmed.columns = ('pubmedid', 'pmcterms')

        comb = self.pd.merge(arxiv, pubmed, how='cross')
        del arxiv, pubmed

        comb['similarity'] = comb[['arxivterms', 'pmcterms']].apply(
            lambda r: self.scalar_udfs.jaccard(r['arxivterms'], r['pmcterms']),
            axis=1
        )
        del comb['arxivterms'], comb['pmcterms']

        return comb.groupby('arxivid').apply(
            lambda g: self.table_udfs.aggregate_top(g, 5, 'similarity')
        ).reset_index(drop=True).dropna()
