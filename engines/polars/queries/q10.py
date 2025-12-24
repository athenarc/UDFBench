import utils
import polars as pl
from typing import Callable

class Q10(utils.PolarsQueryBase):
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

    @property
    def __kmeans__(self) -> Callable[
        [
            pl.DataFrame,
            str,
            str,
            str,
            int,
        ],
        pl.DataFrame
    ]:
        return self.table_udfs.kmeans_iterative

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
        ).join(
            self.__scan_df__(
                dataset_path, 'projects', data_format,
                self.schemas.Projects, (
                    'id',
                    'fundedamount',
                    'currency',
                ),
            ).select(
                pl.col('id').alias('projects_id'),
                pl.col('fundedamount'),
                pl.col('currency'),
            ).filter(
                pl.col('fundedamount') > 0.0
            ),
            left_on='projectid',
            right_on='projects_id',
        ).select(
            pl.col('id'),
            pl.col('type'),
            pl.struct(['fundedamount', 'currency']).map_elements(
                lambda row: self.scalar_udfs.converttoeuro(
                    row['fundedamount'],
                    row['currency']
                ),
                return_dtype=pl.Float64,
            ).alias('fundedamount')
        # Calculate LazyFrame to fix crash on Large dataset
        ).collect().group_by(
            'id',
            'type',
        ).agg(
            pl.when((
                pl.col('fundedamount').is_null() |
                pl.col('fundedamount').is_nan()
            ).all())
            .then(None)
            .otherwise(pl.col('fundedamount').sum())
            .alias('fundedamount')
        ).pipe(
            lambda df: self.__kmeans__(
                df,
                group_by_column='type',
                kmeans_column='fundedamount',
                ids_column='id',
                num_clusters=5,
            ),
        )
