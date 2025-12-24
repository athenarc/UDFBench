import utils
import polars as pl

class Q17(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        stem = self.scalar_udfs.stem
        log_10 = self.scalar_udfs.log_10
        filterstopwords = self.scalar_udfs.filterstopwords
        keywords = self.scalar_udfs.keywords
        lowerize = self.scalar_udfs.lowerize

        artifact_abstracts = self.__scan_df__(
            dataset_path, 'artifact_abstracts', data_format,
            self.schemas.ArtifactAbstracts, (
                'artifactid',
                'abstract',
            ),
        ).collect()
        # polars n_unique skips NaNs by default
        total_docid = artifact_abstracts.select(
            pl.col('artifactid').n_unique()
        ).item(0, 0)

        processed = artifact_abstracts.lazy().filter(
            pl.col('abstract').is_not_null() &
            # Pandas `.notna` skips 'N/A' as well!
            (pl.col('abstract') != 'N/A')
        ).select(
            pl.col('artifactid').alias('docid'),
            pl.col('abstract').map_elements(
                lambda x: stem(filterstopwords(keywords(lowerize(x)))),
                return_dtype=pl.String,
            ).alias('abstract')
        ).filter(
            pl.col('abstract').is_not_null()
        ).select(
            pl.col('docid'),
            pl.col('abstract').map_elements(
                self.table_udfs.strsplitv,
                return_dtype=pl.List(pl.String),
            ).alias('term')
        ).explode('term')

        term_counts = processed.group_by(
            pl.col('term'),
            pl.col('docid'),
        ).agg(
            pl.count().alias('count')
        )        
        total_terms = term_counts.group_by('docid').agg(
            pl.col('count').sum().alias('total_terms')
        )

        return term_counts.join(
            total_terms,
            on='docid',
        ).with_columns(
            (pl.col('count') / pl.col('total_terms')).alias('tf')
        ).select(
            'docid', 'term', 'tf'
        ).map_batches(
            lambda df: self.table_udfs.jgroupordered(
                df,
                order_by_col='term',
                count_col='docid'
            ),
            schema={
                'docid': pl.String,
                'term': pl.String,
                'tf': pl.Float64,
                'jscount': pl.UInt32,
            }
        ).with_columns(
            pl.struct(['jscount', 'tf']).map_elements(
                lambda row: (
                    row['tf'] * (
                        log_10(
                            total_docid * 1.0 / (1.0 + row['jscount'])
                        ) + 1.0
                    )
                ),
                return_dtype=pl.Float64,
            ).alias('tfidf')
        ).select('docid', 'term', 'tfidf',).collect()
