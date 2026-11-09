import utils

class Q24(utils.PandasQueryBase):
    def __init__(self, pd_module, schema_module, **udf_paths):
        super().__init__(pd_module, schema_module, scalar_udf_path=udf_paths['scalar_udf_path'], table_udf_path=udf_paths['table_udf_path'])

    def __exec__(self, _: str, __: utils.SupportedDataFormat, external_data_path: str):
        arxiv = self.table_udfs.file(path=self.__create_data_file_path__(external_data_path, 'arxiv', 'csv'), pd=self.pd, file_type='csv', header=None)
        pubmed = self.table_udfs.file(path=self.__create_data_file_path__(external_data_path, 'pubmed', 'txt'), pd=self.pd, file_type='json', lines=True)
        arxiv = arxiv.loc[arxiv[1].notna()]; pubmed = pubmed.loc[pubmed['abstract'].notna()]
        arxiv.columns = ('arxivid', 'abstract'); pubmed = pubmed.rename(columns={'id': 'pubmedid'})[['pubmedid', 'abstract']]
        comb = self.pd.merge(arxiv, pubmed, how='cross', suffixes=('_arxiv', '_pubmed'))
        comb['similarity'] = comb[['abstract_arxiv', 'abstract_pubmed']].apply(lambda r: self.scalar_udfs.deep_similarity_score(r.iloc[0], r.iloc[1], 'sentence-transformers/all-MiniLM-L6-v2', 'cuda'), axis=1)
        return comb.groupby('arxivid', group_keys=False).apply(
            lambda group: self.table_udfs.aggregate_top(group, 5, 'similarity')
        ).reset_index(drop=True)[['arxivid', 'pubmedid', 'similarity']]
