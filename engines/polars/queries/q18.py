import utils
import polars as pl

class Q18(utils.PolarsQueryBase):
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
        _: str,
        __: utils.SupportedDataFormat,
        external_data_path: str
    ):
        jpack = self.scalar_udfs.jpack
        frequentterms = self.scalar_udfs.frequentterms
        stem = self.scalar_udfs.stem
        filterstopwords = self.scalar_udfs.filterstopwords
        keywords = self.scalar_udfs.keywords

        return pl.LazyFrame([{
            'path': self.__create_data_file_path__(
                external_data_path, 'arxiv.csv'
            ),
            'file_type': 'csv',
            'has_header': False,
            'new_columns': ['arxivid', 'arxivterms'],
            'null_values': ['null'],
        }]).map_batches(
            lambda r: self.table_udfs.file(**r.row(0, named=True)),
            schema={
                'arxivid': pl.String,
                'arxivterms': pl.String,
            }
        ).filter(
            pl.col('arxivterms').is_not_null()
        ).select(
            pl.col('arxivid'),
            pl.col('arxivterms').map_elements(
                lambda v: jpack(frequentterms(
                    stem(filterstopwords(keywords(v))),
                    10
                )),
                return_dtype=pl.String
            )
        ).join(
            pl.LazyFrame([{
                'path': self.__create_data_file_path__(
                    external_data_path, 'pubmed.txt'
                ),
                'file_type': 'json',
                'lines': True,
            }]).map_batches(
                lambda r: self.table_udfs.file(**r.row(0, named=True)),
                schema={
                    'id': pl.String,
                    'abstract': pl.String
                }
            ).filter(
                pl.col('abstract').is_not_null()
            ).select(
                pl.col('id').alias('pubmedid'),
                pl.col('abstract').map_elements(
                    lambda v: jpack(frequentterms(
                        stem(filterstopwords(keywords(v))),
                        10
                    )),
                    return_dtype=pl.String
                ).alias('pmcterms')
            ),
            how='cross',
        ).with_columns(
            pl.struct(['arxivterms', 'pmcterms']).map_elements(
                lambda row: self.scalar_udfs.jaccard(
                    row['arxivterms'], row['pmcterms']
                ),
                return_dtype=pl.Float64,
            ).alias('similarity')
        ).group_by(pl.col('arxivid')).map_groups(
            lambda gdf: gdf.pipe(
                self.table_udfs.aggregate_top,
                5,
                'similarity',
            ).with_columns(
                pl.lit(gdf['arxivid'].item(0)).alias('arxivid')
            ),
            schema={
                "arxivid": pl.String,
                "pubmedid": pl.String,
                "similarity": pl.List(pl.Float64),
                "pmcterms": pl.List(pl.String),
            }
        ).drop_nulls().select(
            pl.col('arxivid'),
            pl.col('pubmedid'),
            pl.col('similarity'),
        ).collect()
