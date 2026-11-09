import utils
import polars as pl


class Q23(utils.PolarsQueryBase):
    def __init__(self, schema_module, **udf_paths):
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
        # ------------------------------------------------------------------
        # ArXiv
        # ------------------------------------------------------------------
        arxiv = (
            self.table_udfs.file(
                path=self.__create_data_file_path__(
                    external_data_path,
                    'arxiv.csv'
                ),
                file_type='csv',
                has_header=False,
                new_columns=[
                    'arxivid',
                    'arxiv_abstract'
                ]
            )
            .filter(
                pl.col('arxiv_abstract').is_not_null()
            )
            .with_columns(
                pl.col('arxiv_abstract')
                .map_batches(
                    lambda batch: pl.Series(self.scalar_udfs.deep_embed(
                        batch.to_list(),
                        'sentence-transformers/all-MiniLM-L6-v2',
                        'cuda'
                    )),
                    return_dtype=pl.String
                )
                .alias('arxiv_embedding')
            )
            .select([
                'arxivid',
                'arxiv_embedding'
            ])
        )

        # ------------------------------------------------------------------
        # PubMed
        # ------------------------------------------------------------------
        pubmed = (
            self.table_udfs.file(
                path=self.__create_data_file_path__(
                    external_data_path,
                    'pubmed.txt'
                ),
                file_type='json',
                lines=True
            )
            .rename({'id': 'pubmedid'})
            .select([
                'pubmedid',
                'abstract'
            ])
            .drop_nulls()
            .with_columns(
                pl.col('abstract')
                .map_batches(
                    lambda batch: pl.Series(self.scalar_udfs.deep_embed(
                        batch.to_list(),
                        'sentence-transformers/all-MiniLM-L6-v2',
                        'cuda'
                    )),
                    return_dtype=pl.String
                )
                .alias('pubmed_embedding')
            )
            .select([
                'pubmedid',
                'pubmed_embedding'
            ])
        )

        # ------------------------------------------------------------------
        # Cartesian product of the already-embedded datasets
        # ------------------------------------------------------------------
        comb = (
            arxiv
            .join(
                pubmed,
                how='cross'
            )
            .with_columns(
                pl.struct([
                    'arxiv_embedding',
                    'pubmed_embedding'
                ])
                .map_elements(
                    lambda r: self.scalar_udfs.deep_cosine(
                        r['arxiv_embedding'],
                        r['pubmed_embedding']
                    ),
                    return_dtype=pl.Float64
                )
                .alias('similarity')
            )
        )

        # ------------------------------------------------------------------
        # Top 5 PubMed matches for each ArXiv artifact
        # ------------------------------------------------------------------
        return (
            comb
            .group_by(
                'arxivid',
                maintain_order=True
            )
            .map_groups(
                lambda group: self.table_udfs.aggregate_top(
                    group,
                    5,
                    'similarity'
                ),
            )
            .select([
                'arxivid',
                'pubmedid',
                'similarity'
            ])
        )
