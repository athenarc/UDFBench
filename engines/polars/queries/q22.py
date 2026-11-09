import utils
import polars as pl


class Q25(utils.PolarsQueryBase):
    def __init__(self, schema_module, **udf_paths):
        super().__init__(
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        S = self.schemas

        # Artifacts
        a = (
            self.__scan_df__(
                dataset_path,
                'artifacts',
                data_format,
                S.Artifacts,
                ('id', 'title', 'date')
            )
            .with_columns(
                pl.col('date')
                .map_elements(
                    self.scalar_udfs.extractyear,
                    return_dtype=pl.Int64
                )
                .alias('year')
            )
        )


        # Number of distinct authors per artifact
        au = (
            self.__scan_df__(
                dataset_path,
                'artifact_authors',
                data_format,
                S.ArtifactAuthors,
                ('artifactid', 'authorid')
            )
            .group_by('artifactid')
            .agg(
                pl.col('authorid')
                .n_unique()
                .alias('author_count')
            )
        )

        # Project-artifact relationships
        pa_df = self.__scan_df__(
            dataset_path,
            'projects_artifacts',
            data_format,
            S.ProjectsArtifacts,
            ('projectid', 'artifactid')
        )

        # Projects
        p = (
            self.__scan_df__(
                dataset_path,
                'projects',
                data_format,
                S.Projects,
                ('id', 'fundingstring')
            )
            .with_columns(
                pl.col('fundingstring')
                .map_elements(
                    self.scalar_udfs.extractfunder,
                    return_dtype=pl.String
                )
                .alias('funder')
            )
            .filter(
                pl.col('funder') == 'FP7'
            )
        )

        # Artifact citations
        ac = self.__scan_df__(
            dataset_path,
            'artifact_citations',
            data_format,
            S.ArtifactCitations,
            ('artifactid', 'citcount')
        )

        # Join all relations
        fofo = (
            a
            .join(
                au,
                left_on='id',
                right_on='artifactid',
                how='inner'
            )
            .join(
                pa_df,
                left_on='id',
                right_on='artifactid',
                how='inner'
            )
            .join(
                p,
                left_on='projectid',
                right_on='id',
                how='inner'
            )
            .join(
                ac,
                left_on='id',
                right_on='artifactid',
                how='left'
            )
            .unique(
                subset=['id'],
                keep='first',
                maintain_order=True
            )
        )

        # Predict impact using the scalar UDF
        fofo = fofo.with_columns(
            pl.struct([
                'author_count',
                'citcount',
                'year'
            ])
            .map_elements(
                lambda r: self.scalar_udfs.dlpredict_citations(
                    r['author_count'],
                    0 if r['citcount'] is None else r['citcount'],
                    r['year'],
                    'cuda'
                ),
                return_dtype=pl.Float64
            )
            .alias('predicted_impact')
        )

        # Sort, take top 20, and return the same columns as Pandas
        result = (
            fofo
            .sort(
                'predicted_impact',
                descending=True
            )
            .head(20)
            .select([
                'id',
                'title',
                'predicted_impact',
                'citcount'
            ]).collect()
        )
        return result
