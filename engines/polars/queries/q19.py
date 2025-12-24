import utils
import polars as pl

class Q19(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str
    ):
        super().__init__(
            schema_module,
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        return self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, (
                'id',
                'type',
            ),
        ).join(
            self.__scan_df__(
                dataset_path, 'projects_artifacts', data_format,
                self.schemas.ProjectsArtifacts, (
                    'projectid',
                    'artifactid',
                ),
            ),
            left_on='id',
            right_on='artifactid',
        ).select(
            pl.col('projectid').alias('pid'),
            pl.col('type').alias('result_type')
        ).collect().pipe(
            self.table_udfs.pivot,
            group_by_column='pid',
            pivot_column='result_type',
            aggregate_function='count'
        )
