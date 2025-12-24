import utils
import polars as pl

class Q15(utils.PolarsQueryBase):
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
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        external_data_path: str
    ):
        artifacts = self.__scan_df__(
            dataset_path, 'artifacts', data_format,
            self.schemas.Artifacts, (
                'id',
            ),
        )
        exclude_pids = artifacts.join(
            self.__scan_df__(
                dataset_path, 'projects_artifacts', data_format,
                self.schemas.ProjectsArtifacts, (
                    'projectid',
                    'artifactid',
                ),
            ),
            left_on='id',
            right_on='artifactid',
        ).join(
            self.__scan_df__(
                dataset_path, 'projects', data_format,
                self.schemas.Projects, (
                    'id',
                    'fundingstring',
                ),
            ),
            left_on='projectid',
            right_on='id',
        ).select(
            pl.col('fundingstring').map_elements(
                self.scalar_udfs.extractcode,
                return_dtype=pl.String,
            ).alias('projectid')
        )

        return pl.LazyFrame(({
            'path': self.__create_data_file_path__(
                external_data_path, 'crossref.xml'
            ),
            'file_type': 'txt'
        },)).map_batches(
            lambda r: self.table_udfs.file(**r.row(0, named=True)),
            schema={'text': pl.String}
        ).map_batches(
            lambda df: self.table_udfs.xmlparser(
                df,
                root_name='publication',
                column_name='text'
            ),
        ).select(
            pl.col('text').map_elements(
                lambda row: self.table_udfs.extractkeys(
                    row,
                    key1='publicationdoi',
                    key2='fundinginfo',
                ),
                return_dtype=pl.List(pl.String),
            ).list.to_struct(fields=('publicationdoi', 'fundinginfo'))
        ).unnest('text').with_columns(
            pl.col('fundinginfo').map_elements(
                self.scalar_udfs.extractprojectid,
                return_dtype=pl.String,
            ).alias('projectid')
        ).join(
            artifacts,
            left_on='publicationdoi',
            right_on='id'
        ).filter(
            ~pl.col('projectid').is_in(exclude_pids.collect()['projectid'])
        ).select(
            pl.col('publicationdoi').alias('id'),
            pl.col('projectid')
        ).collect()
