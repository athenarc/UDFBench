import utils

class Q19(utils.PandasQueryBase):
    def __init__(
        self,
        pd_module,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            pd_module,
            schema_module,
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        Artifacts = self.schemas.Artifacts
        ProjectsArtifacts = self.schemas.ProjectsArtifacts

        st = self.__read_df__(
            dataset_path, 'artifacts',
            [
                Artifacts.id,
                Artifacts.type,
            ],
            data_format
        ).merge(
            self.__read_df__(
                dataset_path, 'projects_artifacts',
                [
                    ProjectsArtifacts.projectid,
                    ProjectsArtifacts.artifactid,
                ],
                data_format
            ),
            left_on=Artifacts.id,
            right_on=ProjectsArtifacts.artifactid,
            suffixes=('_a', '_pa')
        )[[f'{ProjectsArtifacts.projectid}_pa', Artifacts.type]]
        st.columns = ('pid', 'result_type')

        return st.pipe(
            self.table_udfs.pivot,
            group_by_column='pid',
            pivot_column='result_type',
            aggregate_function='size'
        )
