import utils
import polars as pl

class Q16(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
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
        cte_xx = self.__scan_df__(
            dataset_path, 'projects', data_format,
            self.schemas.Projects, (
                'id',
                'startdate',
                'enddate',
                'fundingstring',
            ),
        ).rename({ 'id': 'projectid' }).join(
            self.__scan_df__(
                dataset_path, 'projects_artifacts', data_format,
                self.schemas.ProjectsArtifacts, (
                    'projectid',
                    'artifactid',
                ),
            ),
            on='projectid',
        ).join(
            self.__scan_df__(
                dataset_path, 'artifact_authorlists', data_format,
                self.schemas.ArtifactAuthorlists, (
                    'artifactid',
                    'authorlist',
                ),
            ).with_columns(
                pl.col('authorlist').map_elements(
                    self.scalar_udfs.jsoncount,
                    return_dtype=pl.Int64
                ).alias('authorlist_count')
            ).filter(
                (pl.col('authorlist_count') < 7) |
                pl.col('authorlist_count').is_null()
            ),
            on='artifactid',
        ).join(
            self.__scan_df__(
                dataset_path, 'artifacts', data_format,
                self.schemas.Artifacts, (
                    'id',
                    'date',
                ),
            ).rename({ 'id': 'artifactid' }),
            on='artifactid',
        ).select(
            pl.col('artifactid').alias('pubid'),
            pl.col('date').alias('pubdate'),
            pl.col('startdate').alias('projectstart'),
            pl.col('enddate').alias('projectend'),
            pl.col('fundingstring').map_elements(
                self.scalar_udfs.extractfunder,
                return_dtype=pl.String,
            ).alias('funder'),
            pl.col('fundingstring').map_elements(
                self.scalar_udfs.extractclass,
                return_dtype=pl.String,
            ).alias('class'),
            pl.col('fundingstring').map_elements(
                self.scalar_udfs.extractid,
                return_dtype=pl.String,
            ).alias('projectid'),
            pl.col('authorlist'),
        ).with_columns(
            pl.col('authorlist').map_elements(
                lambda al: self.table_udfs.combinations(
                    self.scalar_udfs.jsort(
                        self.scalar_udfs.jsortvalues(
                            self.scalar_udfs.removeshortterms(
                                self.scalar_udfs.lowerize(al)
                            )
                        )
                    ), 2
                ),
                return_dtype=pl.List(pl.String),
            ).alias('authorpair')
        ).explode('authorpair').drop_nulls(subset=['authorpair'])

        return cte_xx.join(
            cte_xx.filter(pl.col('projectid').is_not_null()),
            on='authorpair',
        ).select(
            pl.col('funder'),
            pl.col('class'),
            pl.col('projectid'),
            pl.col('projectstart').map_elements(
                self.scalar_udfs.cleandate,
                return_dtype=pl.String
            ).alias('pstartcleaned'),
            pl.col('projectend').map_elements(
                self.scalar_udfs.cleandate,
                return_dtype=pl.String
            ).alias('pendcleaned'),
            pl.col('authorpair'),
            pl.col('pubdate'),
        ).group_by('funder', 'class', 'projectid').agg([
            pl.col('pubdate').filter(
                (pl.col('pubdate') >= pl.col('pstartcleaned')) &
                (pl.col('pubdate') <= pl.col('pendcleaned'))
            ).count().alias('authors_during'),
            pl.col('pubdate').filter(
                pl.col('pubdate') < pl.col('pstartcleaned')
            ).count().alias('authors_before'),
            pl.col('pubdate').filter(
                pl.col('pubdate') > pl.col('pendcleaned')
            ).count().alias('authors_after'),
        ]).collect()
        