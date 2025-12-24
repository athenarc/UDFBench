import utils

class Q15(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
            pd_module,
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        external_data_path: str
    ):
        crossref_sub = self.pd.DataFrame([{
            'path': self.__create_data_file_path__(
                dataset_path=external_data_path,
                filename_no_ext='crossref', data_format='xml'
            ),
            'file_type': 'txt',
            'pd': self.pd
        }]).pipe(lambda r: self.table_udfs.file(**r.iloc[0])).pipe(
            self.table_udfs.xmlparser,
            root_name='publication',
            column_name=0,
            pd=self.pd
        ).apply(
            lambda row: self.table_udfs.extractkeys(
                row[0],
                key1='publicationdoi',
                key2='fundinginfo',
            ),            
            axis=1,
            result_type='expand'
        )
        crossref_sub.columns = ('publicationdoi', 'fundinginfo')
        crossref_sub['projectid'] = crossref_sub['fundinginfo'].apply(
            self.scalar_udfs.extractprojectid
        )
        del crossref_sub['fundinginfo']
        crossref = crossref_sub

        Artifacts = self.schemas.Artifacts
        artifacts = self.__read_df__(
            data_format=data_format, dataset_path=dataset_path,
            filename_no_ext='artifacts', usecols=[Artifacts.id]
        )
        ProjectsArtifacts = self.schemas.ProjectsArtifacts
        projects_artifacts = self.__read_df__(
            data_format=data_format, dataset_path=dataset_path,
            filename_no_ext='projects_artifacts', usecols=[
                ProjectsArtifacts.artifactid,
                ProjectsArtifacts.projectid,
            ]
        )
        Projects = self.schemas.Projects
        projects = self.__read_df__(
            data_format=data_format, dataset_path=dataset_path,
            filename_no_ext='projects', usecols=[
                Projects.id,
                Projects.fundingstring,
            ]
        )

        exclude_pids = artifacts.merge(
            projects_artifacts,
            left_on=Artifacts.id,
            right_on=ProjectsArtifacts.artifactid,
            suffixes=('_a', '_pa')
        ).merge(
            projects,
            left_on=f'{ProjectsArtifacts.projectid}_pa',
            right_on=Projects.id,
            suffixes=('_apa', '_p')
        )[Projects.fundingstring].apply(self.scalar_udfs.extractcode)
        exclude_pids.columns = ('projectid',)

        return self.pd.merge(
            crossref.loc[~crossref['projectid'].isin(exclude_pids)],
            artifacts,
            left_on='publicationdoi',
            right_on=Artifacts.id
        )[[Artifacts.id, 'projectid']]
