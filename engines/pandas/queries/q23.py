
import utils

class Q23(utils.PandasQueryBase):
    def __init__(self, pd_module, schema_module, **udf_paths):
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
        arxiv = self.table_udfs.file(
            path=self.__create_data_file_path__(
                external_data_path, 'arxiv', 'csv'
            ),
            pd=self.pd,
            file_type='csv',
            header=None
        )

        pubmed = self.table_udfs.file(
            path=self.__create_data_file_path__(
                external_data_path, 'pubmed', 'txt'
            ),
            pd=self.pd,
            file_type='json',
            lines=True
        )

        arxiv = arxiv.loc[arxiv[1].notna()]
        pubmed = pubmed.loc[pubmed['abstract'].notna()]

        arxiv.columns = ('arxivid', 'abstract')
        pubmed = pubmed.rename(
            columns={'id': 'pubmedid'}
        )[['pubmedid', 'abstract']]

        # Embed each abstract BEFORE the cross join.
        arxiv['embedding'] = arxiv['abstract'].apply(
            lambda x: self.scalar_udfs.deep_embed(
                x,
                'sentence-transformers/all-MiniLM-L6-v2',
                'cuda'
            )
        )

        pubmed['embedding'] = pubmed['abstract'].apply(
            lambda x: self.scalar_udfs.deep_embed(
                x,
                'sentence-transformers/all-MiniLM-L6-v2',
                'cuda'
            )
        )

        # Cartesian product of the already-embedded rows.
        comb = self.pd.merge(
            arxiv[['arxivid', 'embedding']],
            pubmed[['pubmedid', 'embedding']],
            how='cross',
            suffixes=('_arxiv', '_pubmed')
        )

        # Cosine similarity now operates directly on the precomputed
        # embeddings; no embedding UDFs are executed after the cross join.
        comb['similarity'] = comb.apply(
            lambda r: self.scalar_udfs.deep_cosine(
                r['embedding_arxiv'],
                r['embedding_pubmed']
            ),
            axis=1
        )

        return (
            comb.groupby('arxivid')
            .apply(
                lambda group: self.table_udfs.aggregate_top(
                    group,
                    5,
                    'similarity'
                )
            )
            .reset_index(drop=True)[
                ['arxivid', 'pubmedid', 'similarity']
            ]
        )


