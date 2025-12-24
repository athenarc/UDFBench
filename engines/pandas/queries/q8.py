import utils

class Q8(utils.PandasQueryBase):
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
            aggr_udf_path=udf_paths['aggr_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        pd = self.pd
        ArtifactCitations = self.schemas.ArtifactCitations
        ArtifactAuthorlists = self.schemas.ArtifactAuthorlists
        citations = self.__read_df__(
            dataset_path, 'artifact_citations',
            [
                ArtifactCitations.artifactid,
                ArtifactCitations.target
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
        # To avoid null joins
        # citations.dropna(subset=[ArtifactCitations.artifactid])
        # authorlists.dropna(subset=[ArtifactAuthorlists.artifactid])
        joined_data = pd.merge(
            citations, authorlists,
            left_on=ArtifactCitations.artifactid,
            right_on=ArtifactAuthorlists.artifactid,
            suffixes=('_citations', '_authorlists')
        )
        return pd.DataFrame((
            joined_data[f'{ArtifactCitations.target}_citations'].apply(
                self.scalar_udfs.jsoncount
            ).pipe(self.aggr_udfs.aggregate_avg),
            joined_data[f'{ArtifactAuthorlists.authorlist}_authorlists'].apply(
                self.scalar_udfs.jsoncount
            ).pipe(self.aggr_udfs.aggregate_avg),
        )).T
