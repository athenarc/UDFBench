import utils

class Q10Bench(utils.PandasQueryBase):
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
        _: str
    ):
        Artifacts = self.schemas.Artifacts
        Projects = self.schemas.Projects
        ProjectsArtifacts = self.schemas.ProjectsArtifacts
        artifacts = self.__time_fn__(
            lambda: self.__read_df__(
                dataset_path, 'artifacts',
                [
                    Artifacts.id,
                    Artifacts.type,
                ],
                data_format
            ),
            'read artifacts'
        )
        projects = self.__time_fn__(
            lambda: self.__read_df__(
                dataset_path, 'projects',
                [
                    Projects.id,
                    Projects.fundedamount,
                    Projects.currency,
                ],
                data_format
            ),
            'read projects'
        )
        projects_artifacts = self.__time_fn__(
            lambda: self.__read_df__(
                dataset_path, 'projects_artifacts',
                [
                    ProjectsArtifacts.projectid,
                    ProjectsArtifacts.artifactid,
                ],
                data_format
            ),
            'read projects_artifacts'
        )
        converttoeuro = self.scalar_udfs.converttoeuro

        sub_df = self.__time_fn__(
            lambda: artifacts.merge(
                projects_artifacts,
                left_on=Artifacts.id,
                right_on=ProjectsArtifacts.artifactid,
                suffixes=('_a', '_pa')
            ),
            'merge artifacts with projects_artifacts'
        )
        sub_df = self.__time_fn__(
            lambda: sub_df.merge(
                projects[projects[Projects.fundedamount] > 0.0],
                left_on=f'{ProjectsArtifacts.projectid}_pa',
                right_on=Projects.id,
                suffixes=('_apa', '_p')
            ),
            'merge j1 with projects'
        )
        
        converttoeuro = self.__time_fn__(
            lambda: sub_df[[Projects.fundedamount, Projects.currency]].apply(
                lambda row: converttoeuro(
                    row[Projects.fundedamount],
                    row[Projects.currency]
                ),
                axis=1
            ),
            'converttoeuro'
        )
        sub_df = self.__time_fn__(
            lambda: self.pd.concat([
                sub_df[f'{Artifacts.id}_a'],
                sub_df[Artifacts.type],
                converttoeuro
            ], axis=1),
            'concat columns'
        )
        sub_df.columns = ('id', 'type', 'fundedamount')
        sub_df.reset_index(inplace=True)
        
        groupby = self.__time_fn__(
            lambda: sub_df.groupby(
                ['id', 'type'], as_index=False
            ),
            'groupby'
        )
        agg = self.__time_fn__(
            lambda: groupby.agg({
                'fundedamount': lambda fa: fa.sum(min_count=1)
            }),
            'fundedamount group sum'
        )
        return self.__time_fn__(
            lambda: agg.pipe(
                self.table_udfs.kmeans_iterative,
                group_by_column='type',
                kmeans_column='fundedamount',
                ids_column='id',
                num_clusters=5,
                pd=self.pd,
            ),
            'kmeans_iterative'
        )
