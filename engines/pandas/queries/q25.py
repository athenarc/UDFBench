import utils
import json

class Q29(utils.PandasQueryBase):

    def __init__(self, pd_module, schema_module, **udf_paths):
        super().__init__(
            pd_module,
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            aggr_udf_path=udf_paths['aggr_udf_path']
        )

    def __exec__(self, dataset_path, data_format, _):
        pd, S = self.pd, self.schemas

        # ---------------------------------------------------------
        # Projects
        # ---------------------------------------------------------
        projects = self.__read_df__(
            dataset_path,
            'projects',
            [
                S.Projects.id,
                S.Projects.fundingstring
            ],
            data_format
        )

        projects = projects.rename(columns={
            S.Projects.id: 'project_id',
            S.Projects.fundingstring: 'fundingstring'
        })

        # ---------------------------------------------------------
        # Projects <-> Artifacts links
        # ---------------------------------------------------------
        links = self.__read_df__(
            dataset_path,
            'projects_artifacts',
            [
                S.ProjectsArtifacts.projectid,
                S.ProjectsArtifacts.artifactid
            ],
            data_format
        )

        links = links.rename(columns={
            S.ProjectsArtifacts.projectid: 'project_id',
            S.ProjectsArtifacts.artifactid: 'artifact_id'
        })

        # ---------------------------------------------------------
        # Artifacts
        # ---------------------------------------------------------
        artifacts = self.__read_df__(
            dataset_path,
            'artifacts',
            [
                S.Artifacts.id,
                S.Artifacts.date
            ],
            data_format
        )

        artifacts = artifacts.rename(columns={
            S.Artifacts.id: 'artifact_id',
            S.Artifacts.date: 'date'
        })

        # Keep artifacts after 2020
        artifacts = artifacts[
            artifacts['date'].map(
                self.scalar_udfs.extractyear
            ) > 2020
        ]

        # ---------------------------------------------------------
        # Abstracts
        # ---------------------------------------------------------
        abstracts = self.__read_df__(
            dataset_path,
            'artifact_abstracts',
            [
                S.ArtifactAbstracts.artifactid,
                S.ArtifactAbstracts.abstract
            ],
            data_format
        )

        abstracts = abstracts.rename(columns={
            S.ArtifactAbstracts.artifactid: 'artifact_id',
            S.ArtifactAbstracts.abstract: 'abstract'
        })

        # ---------------------------------------------------------
        # Joins
        # ---------------------------------------------------------
        rows = (
            projects
            .merge(
                links,
                on='project_id'
            )
            .merge(
                artifacts,
                on='artifact_id'
            )
            .merge(
                abstracts,
                on='artifact_id'
            )
        )

        # ---------------------------------------------------------
        # Remove artifacts without an abstract
        # ---------------------------------------------------------
        rows = rows[
            rows['abstract'].notna()
        ]

        # ---------------------------------------------------------
        # Extract funder
        # ---------------------------------------------------------
        rows['funder'] = rows['fundingstring'].map(
            self.scalar_udfs.extractfunder
        )
        #print(rows)
        # ---------------------------------------------------------
        # Aggregate embeddings per funder
        # ---------------------------------------------------------
        result = (
            rows
            .groupby(
                'funder',
                dropna=False
            )['abstract']
            .apply(
                lambda texts: self.aggr_udfs.dl_embed_agg(
                    texts,
                    'sentence-transformers/all-MiniLM-L6-v2',
                    'cuda'
                )
            )
            .reset_index(
                name='funder_embedding'
            )
        )
        print(result)
        return result
