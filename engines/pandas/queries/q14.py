import utils

class Q14(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
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
        pd = self.pd
        Artifacts = self.schemas.Artifacts
        ArtifactAuthors = self.schemas.ArtifactAuthors
        Projects = self.schemas.Projects
        ProjectsArtifacts = self.schemas.ProjectsArtifacts

        artifact_authors = self.__read_df__(
            dataset_path, 'artifact_authors',
            [
                ArtifactAuthors.artifactid,
                ArtifactAuthors.affiliation,
                ArtifactAuthors.rank,
                ArtifactAuthors.authorid,
            ],
            data_format
        )
        
        artifacts = self.__read_df__(
            dataset_path, 'artifacts',
            [
                Artifacts.id,
                Artifacts.date,
            ],
            data_format
        )

        projects = self.__read_df__(
            dataset_path, 'projects',
            [
                Projects.id,
                Projects.funder,
            ],
            data_format
        )
        
        projects_artifacts = self.__read_df__(
            dataset_path, 'projects_artifacts',
            [
                ProjectsArtifacts.projectid,
                ProjectsArtifacts.artifactid,
            ],
            data_format
        )
        cte_df = artifact_authors.loc[
            (artifact_authors[ArtifactAuthors.affiliation].notna())
            & (artifact_authors[ArtifactAuthors.affiliation] != '[]')
            & (artifact_authors[ArtifactAuthors.authorid].notna())
            & (artifact_authors[ArtifactAuthors.authorid] != '[]')
            , [
                ArtifactAuthors.artifactid,
                ArtifactAuthors.authorid,
                ArtifactAuthors.affiliation,
                ArtifactAuthors.rank,
            ]
        ]
        cte_df[[
            'authoridvalue',
            'affiliationvalue'
        ]] = cte_df.loc[:, [
            ArtifactAuthors.authorid,
            ArtifactAuthors.affiliation
        ]].apply(
            lambda row: pd.Series((
                self.scalar_udfs.jsonparse_q14(
                    row[ArtifactAuthors.authorid], 'value'
                ),
                self.scalar_udfs.jsonparse_q14(
                    row[ArtifactAuthors.affiliation], 'value'
                ),
            )), axis=1
        )
        cte_df.rename(columns={
            ArtifactAuthors.artifactid: 'artifactid',
            ArtifactAuthors.authorid: 'authorid',
            ArtifactAuthors.affiliation: 'affiliation',
            ArtifactAuthors.rank: 'rank',
        }, inplace=True)

        sub_df = pd.merge(
            artifact_authors.loc[
                artifact_authors[ArtifactAuthors.rank] == 1,
                [
                    ArtifactAuthors.artifactid,
                    ArtifactAuthors.authorid,
                ]
            ],
            artifacts.loc[:, [
                Artifacts.id,
                Artifacts.date
            ]],
            left_on=ArtifactAuthors.artifactid,
            right_on=Artifacts.id,
            suffixes=('_aa', '_a')
        ).apply(
            lambda row: pd.Series([
                row[ArtifactAuthors.authorid],
                self.scalar_udfs.cleandate(row[Artifacts.date])
            ]), axis=1
        )
        # sub_df[Artifacts.date] = sub_df[Artifacts.date].apply(cleandate)
        sub_df.dropna(inplace=True, subset=[1])
        author_groupby = self.pd.DataFrame(sub_df.groupby([0]).apply(
            lambda group_df: self.aggr_udfs.aggregate_max(group_df[1])
        ), columns=[1])
        author_groupby.reset_index(inplace=True)

        temp = cte_df.loc[cte_df['rank'] == 1].merge(
            artifacts,
            left_on='artifactid',
            right_on=Artifacts.id,
        ).merge(
            projects_artifacts,
            left_on='artifactid',
            right_on=ProjectsArtifacts.artifactid,
            suffixes=('_temp', '_pa')
        ).merge(
            projects.loc[projects[Projects.funder] == 'European Commission'],
            left_on=f'{ProjectsArtifacts.projectid}_pa',
            right_on=Projects.id,
            suffixes=('_temp', '_projects')
        )
        temp[Artifacts.date] = temp[Artifacts.date].apply(
            self.scalar_udfs.cleandate
        )        
        
        return temp.merge(
            author_groupby[[0, 1]],
            left_on=['authorid', Artifacts.date],
            right_on=[0, 1],
            suffixes=('_final', '_sub_df_groupby')
        )[[
            'authoridvalue',
            'affiliationvalue'
        ]]
