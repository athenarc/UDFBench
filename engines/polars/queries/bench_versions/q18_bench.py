import utils
import polars as pl

class Q18Bench(utils.PolarsQueryBase):
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

        arxiv = self.__time_fn__(
            lambda: pl.LazyFrame([{
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
            ).collect(),
            'arxiv file UDF',
        ).lazy()

        arxiv = self.__time_fn__(
            lambda: arxiv.filter(
                pl.col('arxivterms').is_not_null()
            ).collect(),
            'filter non null arxivterms',
        ).lazy()

        arxiv_udfs = self.__time_fn__(
            lambda: arxiv.select(
                pl.col('arxivid'),
                pl.col('arxivterms').map_elements(
                    lambda v: jpack(frequentterms(
                        stem(filterstopwords(keywords(v))),
                        10
                    )),
                    return_dtype=pl.String
                )
            ).collect(),
            'arxiv UDFs',
        ).lazy()

        pubmed = self.__time_fn__(
            lambda: pl.LazyFrame([{
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
            ).collect(),
            'pubmed file UDF',
        ).lazy()

        pubmed = self.__time_fn__(
            lambda: pubmed.filter(
                pl.col('abstract').is_not_null()
            ).collect(),
            'filter non null abstract',
        ).lazy()

        pubmed_udfs = self.__time_fn__(
            lambda: pubmed.select(
                pl.col('id').alias('pubmedid'),
                pl.col('abstract').map_elements(
                    lambda v: jpack(frequentterms(
                        stem(filterstopwords(keywords(v))),
                        10
                    )),
                    return_dtype=pl.String
                ).alias('pmcterms')
            ).collect(),
            'pubmed UDFs',
        ).lazy()

        cross = self.__time_fn__(
            lambda: arxiv_udfs.join(
                pubmed_udfs,
                how='cross',
            ).collect(),
            'cross join arxiv and pubmed',
        ).lazy()

        jaccard = self.__time_fn__(
            lambda: cross.with_columns(
                pl.struct(['arxivterms', 'pmcterms']).map_elements(
                    lambda row: self.scalar_udfs.jaccard(
                        row['arxivterms'], row['pmcterms']
                    ),
                    return_dtype=pl.Float64,
                ).alias('similarity')
            ).collect(),
            'jaccard similarity',
        )

        groupby = self.__time_fn__(
            lambda: jaccard.group_by('arxivid'),
            'group by',
        )

        return self.__time_fn__(
            lambda: groupby.map_groups(
                lambda gdf: gdf.pipe(
                    self.table_udfs.aggregate_top,
                    5,
                    'similarity',
                ).with_columns(
                    pl.lit(gdf['arxivid'].item(0)).alias('arxivid')
                ),
                # schema={
                #     "arxivid": pl.String,
                #     "pubmedid": pl.String,
                #     "similarity": pl.List(pl.Float64),
                #     "pmcterms": pl.List(pl.String),
                # }
            # After testing in Eager mode, `drop_nulls` filters out a few more rows,
            # resulting in different total rows (in Medium & Large datasets)
            ),
            # ).drop_nulls(),
            'aggregate top',
        ).select(
            pl.col('arxivid'),
            pl.col('pubmedid'),
            pl.col('similarity'),
        )
