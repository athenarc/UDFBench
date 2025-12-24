import utils

class Q16(utils.PandasQueryBase):
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
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        pd = self.pd
        scalar = self.scalar_udfs
        combinations = self.table_udfs.combinations

        Artifacts = self.schemas.Artifacts
        Projects = self.schemas.Projects
        ProjectsArtifacts = self.schemas.ProjectsArtifacts
        ArtifactAuthorlists = self.schemas.ArtifactAuthorlists

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
                Projects.startdate,
                Projects.enddate,
                Projects.fundingstring,
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
        authorlists = self.__read_df__(
            dataset_path, 'artifact_authorlists',
            [
                ArtifactAuthorlists.artifactid,
                ArtifactAuthorlists.authorlist
            ],
            data_format
        )

        cte_xx = projects.merge(
            projects_artifacts,
            left_on=Projects.id,
            right_on=ProjectsArtifacts.projectid,
            suffixes=('_p', '_pa'),
        ).merge(
            authorlists.loc[
                authorlists[ArtifactAuthorlists.authorlist].apply(
                    lambda d: (scalar.jsoncount(d) or 0) < 7
                )
            ],
            left_on=ProjectsArtifacts.artifactid,
            right_on=ArtifactAuthorlists.artifactid,
            suffixes=('_ppa', '_al')
        ).merge(
            artifacts,
            left_on=f'{ProjectsArtifacts.artifactid}_ppa',
            right_on=Artifacts.id,
            suffixes=('_final', '_a')
        )

        cte_xx = pd.concat((i for i in cte_xx.apply(lambda r: pd.merge(
            pd.DataFrame(({
                'pubid': r[f'{ArtifactAuthorlists.artifactid}_al'],
                'pubdate': r[f'{Artifacts.date}_a'],
                'projectstart': r[Projects.startdate],
                'projectend': r[Projects.enddate],
                'funder': scalar.extractfunder(r[f'{Projects.fundingstring}_final']),
                'class': scalar.extractclass(r[f'{Projects.fundingstring}_final']),
                'projectid': scalar.extractid(r[f'{Projects.fundingstring}_final']),
            }, )),
            pd.DataFrame(combinations(
                scalar.jsort(
                    scalar.jsortvalues(
                        scalar.removeshortterms(
                            scalar.lowerize(r[f'{ArtifactAuthorlists.authorlist}_al'])
                        )
                    )
                ), 2
            ), columns=['authorpair']),
            how='cross'
        ), axis=1)))
        pairs = cte_xx

        sub_xx = pairs.merge(
            pairs.loc[pairs['projectid'].notna()],
            left_on='authorpair',
            right_on='authorpair',
            suffixes=('_pp', '_p')
        )
        sub_xx = pd.DataFrame({
            'funder': sub_xx['funder_pp'],
            'class': sub_xx['class_pp'],
            'projectid': sub_xx['projectid_pp'],
            'pstartcleaned': sub_xx['projectstart_pp'].apply(scalar.cleandate),
            'pendcleaned': sub_xx['projectend_pp'].apply(scalar.cleandate),
            'authorpair': sub_xx['authorpair'],
            'pubdate': sub_xx['pubdate_p'],
        })
        
        sub_xx['authors_during'] = sub_xx['pubdate'].between(
            sub_xx['pstartcleaned'], sub_xx['pendcleaned']
        )
        sub_xx['authors_before'] = sub_xx['pubdate'] < sub_xx['pstartcleaned']
        sub_xx['authors_after'] = sub_xx['pubdate'] > sub_xx['pendcleaned']

        return sub_xx.groupby(
            by=['funder', 'class', 'projectid'],
            as_index=False
        ).agg({
            'authors_during': 'sum',
            'authors_before': 'sum',
            'authors_after': 'sum'
        })
        