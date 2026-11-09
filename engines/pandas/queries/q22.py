import utils


class Q25(utils.PandasQueryBase):
    def __init__(self, pd_module, schema_module, **udf_paths):
        super().__init__(
            pd_module,
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        pd = self.pd
        S = self.schemas

        a = self.__read_df__(
            dataset_path,
            'artifacts',
            [
                S.Artifacts.id,
                S.Artifacts.title,
                S.Artifacts.date
            ],
            data_format
        ).rename(columns={
            S.Artifacts.id: 'id',
            S.Artifacts.title: 'title',
            S.Artifacts.date: 'date'
        })


        au = self.__read_df__(
            dataset_path,
            'artifact_authors',
            [
                S.ArtifactAuthors.artifactid,
                S.ArtifactAuthors.authorid
            ],
            data_format
        ).rename(columns={
            S.ArtifactAuthors.artifactid: 'artifactid',
            S.ArtifactAuthors.authorid: 'authorid'
        })

        pa = self.__read_df__(
            dataset_path,
            'projects_artifacts',
            [
                S.ProjectsArtifacts.projectid,
                S.ProjectsArtifacts.artifactid
            ],
            data_format
        ).rename(columns={
            S.ProjectsArtifacts.projectid: 'projectid',
            S.ProjectsArtifacts.artifactid: 'artifactid'
        })

        p = self.__read_df__(
            dataset_path,
            'projects',
            [
                S.Projects.id,
                S.Projects.fundingstring
            ],
            data_format
        ).rename(columns={
            S.Projects.id: 'id',
            S.Projects.fundingstring: 'fundingstring'
        })

        ac = self.__read_df__(
            dataset_path,
            'artifact_citations',
            [
                S.ArtifactCitations.artifactid,
                S.ArtifactCitations.citcount
            ],
            data_format
        ).rename(columns={
            S.ArtifactCitations.artifactid: 'artifactid',
            S.ArtifactCitations.citcount: 'citcount'
        })

        # Number of distinct authors per artifact
        counts = (
            au
            .groupby('artifactid', as_index=False)['authorid']
            .nunique()
            .rename(columns={
                'artifactid': 'id',
                'authorid': 'author_count'
            })
        )

        # Extract year from artifact date using the scalar UDF
        a['year'] = a['date'].apply(
            self.scalar_udfs.extractyear
        )

        # Rename artifact ID to the common join key

        pa = pa.rename(columns={
            'artifactid': 'id'
        })

        # Extract funder from funding string using the scalar UDF
        p['funder'] = p['fundingstring'].apply(
            self.scalar_udfs.extractfunder
        )

        p = (
            p[p['funder'] == 'FP7']
            .rename(columns={
                'id': 'projectid'
            })
        )

        ac = ac.rename(columns={
            'artifactid': 'id'
        })

        # Join all relations
        fofo = (
            a
            .merge(counts, on='id')
            .merge(pa, on='id')
            .merge(p, on='projectid')
            .merge(ac, on='id', how='left')
            .drop_duplicates('id')
        )

        # Predict impact using the scalar UDF
        fofo['predicted_impact'] = fofo.apply(
            lambda r: self.scalar_udfs.dlpredict_citations(
                r['author_count'],
                r['citcount'] if pd.notna(r['citcount']) else 0,
                r['year'],
                'cuda'
            ),
            axis=1
        )
        return (
            fofo
            .sort_values(
                'predicted_impact',
                ascending=False
            )
            .head(20)[
                [
                    'id',
                    'title',
                    'predicted_impact',
                    'citcount'
                ]
            ]
        )
