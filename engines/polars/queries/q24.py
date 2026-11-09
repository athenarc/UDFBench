import utils
import polars as pl


class Q24(utils.PolarsQueryBase):
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
        arxiv = (
            self.table_udfs.file(
                path=self.__create_data_file_path__(
                    external_data_path,
                    'arxiv.csv'
                ),
                file_type='csv',
                has_header=False,
                new_columns=['arxivid', 'arxiv_abstract']
            )
            .filter(
                pl.col('arxiv_abstract').is_not_null()
            )
        )

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
            .select(['pubmedid', 'abstract'])
            .drop_nulls()
        )

        comb = (
            arxiv
            .join(pubmed, how='cross')
            .with_columns(
                pl.struct([
                    'arxiv_abstract',
                    'abstract'
                ])
                .map_elements(
                    lambda r: self.scalar_udfs.deep_similarity_score(
                        r['arxiv_abstract'],
                        r['abstract'],
                        'sentence-transformers/all-MiniLM-L6-v2',
                        'cuda'
                    ),
                    return_dtype=pl.Float64
                )
                .alias('similarity')
            )
        )

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
                )
            )
            .select([
                'arxivid',
                'pubmedid',
                'similarity'
            ])
        )
