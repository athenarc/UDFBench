import utils
import polars as pl

class Q8(utils.PolarsQueryBase):
    def __init__(
        self,
        schema_module,
        **udf_paths: str,
    ):
        super().__init__(
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
        return self.__scan_df__(
            dataset_path, 'artifact_citations', data_format,
            self.schemas.ArtifactCitations, (
                'artifactid',
                'target'
            ),
        ).join(
            self.__scan_df__(
                dataset_path, 'artifact_authorlists', data_format,
                self.schemas.ArtifactAuthorlists, (
                    'artifactid',
                    'authorlist'
                ),
            ),
            on='artifactid',
        ).select((
            pl.col(c)
                .map_elements(
                    self.scalar_udfs.jsoncount,
                    return_dtype=pl.Int64,
                )
                .drop_nulls()
                .map_batches(
                    self.aggr_udfs.aggregate_avg,
                    return_dtype=pl.Float64,
                    returns_scalar=True,
                )
            for c in ('target', 'authorlist')
        )).collect()
