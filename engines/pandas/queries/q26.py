import utils

class Q27(utils.PandasQueryBase):
    def __init__(self, pd_module, schema_module, **udf_paths):
        super().__init__(
            pd_module,
            schema_module,
            scalar_udf_path=udf_paths['scalar_udf_path'],
            table_udf_path=udf_paths['table_udf_path']
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        pd = self.pd
        S = self.schemas

        # artifact_authors
        au = self.__read_df__(
            dataset_path,
            'artifact_authors',
            [
                S.ArtifactAuthors.artifactid,
                S.ArtifactAuthors.fullname,
                S.ArtifactAuthors.affiliation,
                S.ArtifactAuthors.rank
            ],
            data_format
        )

        au.columns = [
            'artifact_id',
            'raw_name',
            'raw_affil',
            'rank'
        ]

        # artifacts
        a = self.__read_df__(
            dataset_path,
            'artifacts',
            [
                S.Artifacts.id,
                S.Artifacts.date
            ],
            data_format
        )

        a.columns = [
            'artifact_id',
            'event_date'
        ]

        # artifact_abstracts
        ab = self.__read_df__(
            dataset_path,
            'artifact_abstracts',
            [
                S.ArtifactAbstracts.artifactid,
                S.ArtifactAbstracts.abstract
            ],
            data_format
        )

        ab.columns = [
            'artifact_id',
            'abstract'
        ]

        # artifact_authorlists
        al = self.__read_df__(
            dataset_path,
            'artifact_authorlists',
            [
                S.ArtifactAuthorlists.artifactid,
                S.ArtifactAuthorlists.authorlist
            ],
            data_format
        )

        al.columns = [
            'artifact_id',
            'coauthors'
        ]

        # Equivalent to:
        #
        # FROM artifact_authors au
        # JOIN artifacts a ON a.id = au.artifactid
        # JOIN artifact_abstracts ab ON ab.artifactid = au.artifactid
        # LEFT JOIN artifact_authorlists al ON al.artifactid = au.artifactid
        #
        # WHERE au.rank = 1
        #   AND extractyear(a.date) = 2010

        rows = (
            au[au['rank'] == 1]
            .merge(a, on='artifact_id', how='inner')
            .merge(ab, on='artifact_id', how='inner')
            .merge(al, on='artifact_id', how='left')
        )

        # Equivalent to:
        #
        # extractyear(a.date) = 2010
        rows = rows[
            rows['event_date'].apply(
                self.scalar_udfs.extractyear
            ) == 2010
        ]

        # Equivalent to:
        #
        # blockkey(au.fullname, au.affiliation)
        rows['bkey'] = rows.apply(
            lambda r: self.scalar_udfs.blockkey(
                r['raw_name'],
                r['raw_affil']
            ),
            axis=1
        )

        # Equivalent to:
        #
        # COALESCE(al.authorlist, '[]')
        rows['coauthors'] = rows['coauthors'].fillna('[]')

        # Equivalent to:
        #
        # jsoncount(COALESCE(al.authorlist, '[]')) < 5
        rows['author_count'] = rows['coauthors'].apply(
            self.scalar_udfs.jsoncount
        )

        rows = rows[rows['author_count'] < 5]

        # Equivalent to:
        #
        # frequentterms(
        #     stem(
        #         filterstopwords(
        #             keywords(ab.abstract)
        #         )
        #     ),
        #     10
        # )
        rows['topic_terms'] = rows['abstract'].apply(
            lambda value: self.scalar_udfs.frequentterms(
                self.scalar_udfs.stem(
                    self.scalar_udfs.filterstopwords(
                        self.scalar_udfs.keywords(value)
                    )
                ),
                10
            )
        )

        # Equivalent to:
        #
        # unnest(resolveauthors(
        #     SELECT ...
        # ))
        return self.table_udfs.resolveauthors(
            rows[
                [
                    'artifact_id',
                    'bkey',
                    'raw_name',
                    'raw_affil',
                    'coauthors',
                    'topic_terms',
                    'event_date'
                ]
            ],
            'sentence-transformers/all-MiniLM-L6-v2',
            'cpu',
            pd
        )
