import utils
import polars as pl

class Q29(utils.PolarsQueryBase):
    def __init__(self, schema_module, **udf_paths):
        super().__init__(schema_module, scalar_udf_path=udf_paths['scalar_udf_path'], aggr_udf_path=udf_paths['aggr_udf_path'])
    def __exec__(self, dataset_path, data_format, _):
        projects = self.__scan_df__(dataset_path, 'projects', data_format, self.schemas.Projects, ('id', 'fundingstring'))
        links = self.__scan_df__(dataset_path, 'projects_artifacts', data_format, self.schemas.ProjectsArtifacts, ('projectid', 'artifactid'))
        artifacts = self.__scan_df__(dataset_path, 'artifacts', data_format, self.schemas.Artifacts, ('id', 'date')).filter(
            pl.col('date').map_elements(self.scalar_udfs.extractyear, return_dtype=pl.Int64) > 2020
        )
        abstracts = self.__scan_df__(dataset_path, 'artifact_abstracts', data_format, self.schemas.ArtifactAbstracts, ('artifactid', 'abstract'))
        rows = projects.join(links, left_on='id', right_on='projectid').join(artifacts, left_on='artifactid', right_on='id').join(abstracts, on='artifactid').filter(pl.col('abstract').is_not_null()).with_columns(
            pl.col('fundingstring').map_elements(self.scalar_udfs.extractfunder, return_dtype=pl.String).alias('funder'),
        ).select('funder', 'abstract').collect()
        return rows.group_by('funder').map_groups(
            lambda group: pl.DataFrame({'funder': [group['funder'][0]], 'funder_embedding': [self.aggr_udfs.dl_embed_agg(group['abstract'], 'sentence-transformers/all-MiniLM-L6-v2', 'cuda')]})
        )

