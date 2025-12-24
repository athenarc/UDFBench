import utils
import polars as pl

class Q14(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            aggr_udf_path=udf_paths['aggr_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ): 
        artifacts = self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, (
                'id',
                'date',
            ),
        )
        projects = self.__scan_df__(
            dataset_path, 'projects', data_format,
            self.schemas.Projects, (
                'id',
                'funder',
            ),
        )
        projects_artifacts = self.__scan_df__(
            dataset_path, 'projects_artifacts', data_format,
            self.schemas.ProjectsArtifacts, (
                'projectid',
                'artifactid',
            ),
        )
        artifact_authors = self.__scan_df__(
            dataset_path, 'artifact_authors', data_format,
            self.schemas.ArtifactAuthors, (
                'artifactid',
                'authorid',
                'affiliation',
                'rank',
            ),
        )

        cte = artifact_authors.filter(
            pl.col('affiliation').is_not_null() &
            (pl.col('affiliation') != '[]') &
            pl.col('authorid').is_not_null() &
            (pl.col('authorid') != '[]')
        ).with_columns(
            pl.col('authorid').map_elements(
                lambda a: self.scalar_udfs.jsonparse_q14(a, 'value'),
                return_dtype=pl.String
            ).alias('authoridvalue'),
            pl.col('affiliation').map_elements(
                lambda a: self.scalar_udfs.jsonparse_q14(a, 'value'),
                return_dtype=pl.String
            ).alias('affiliationvalue'),
        )

        return cte.filter(
            pl.col('rank') == 1
        ).join(
            artifacts.rename({ 'id': 'artifactid', }),
            on='artifactid',
        ).join(
            projects_artifacts,
            on='artifactid',
        ).join(
            projects.filter(
                pl.col('funder') == 'European Commission'
            ).rename({
                'id': 'projectid',
            }),
            on='projectid',
        ).with_columns(
            pl.col('date').map_elements(
                self.scalar_udfs.cleandate,
                return_dtype=pl.String
            )
        ).join(
            artifact_authors.filter(
                pl.col('rank') == 1
            ).select(
                pl.col('artifactid'),
                pl.col('authorid'),
            ).join(
                artifacts.select(
                    pl.col('id').alias('artifactid'),
                    pl.col('date'),
                ),
                on='artifactid',
            ).select(
                pl.col('authorid'),
                pl.col('date').map_elements(
                    self.scalar_udfs.cleandate,
                    return_dtype=pl.String
                )
            ).drop_nulls(subset=['date']).group_by(
                'authorid'
            ).map_groups(
                lambda gdf: gdf.select(
                    pl.col('authorid').get(0),
                    pl.col('date').map_batches(
                        self.aggr_udfs.aggregate_max,
                        return_dtype=pl.String
                    )
                ),
                schema={
                    'authorid': pl.String,
                    'date': pl.String,
                }
            ),
            on=['authorid', 'date'],
        ).select(
            pl.col('authoridvalue'),
            pl.col('affiliationvalue')
        ).collect()
