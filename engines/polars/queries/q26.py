
import utils
import polars as pl


class Q27(utils.PolarsQueryBase):
    def __init__(self, schema_module, **udf_paths):
        super().__init__(
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
        S = self.schemas

        # ------------------------------------------------------------
        # artifact_authors
        #
        # WHERE au.rank = 1
        # ------------------------------------------------------------

        au = (
            self.__scan_df__(
                dataset_path,
                'artifact_authors',
                data_format,
                S.ArtifactAuthors,
                ('artifactid', 'fullname', 'affiliation', 'rank')
            )
            .filter(
                pl.col('rank') == 1
            )
        )

        # ------------------------------------------------------------
        # artifacts
        # ------------------------------------------------------------

        a = self.__scan_df__(
            dataset_path,
            'artifacts',
            data_format,
            S.Artifacts,
            ('id', 'date')
        )

        # ------------------------------------------------------------
        # artifact_authorlists
        # ------------------------------------------------------------

        al = self.__scan_df__(
            dataset_path,
            'artifact_authorlists',
            data_format,
            S.ArtifactAuthorlists,
            ('artifactid', 'authorlist')
        )

        # ------------------------------------------------------------
        # artifact_abstracts
        # ------------------------------------------------------------

        ab = self.__scan_df__(
            dataset_path,
            'artifact_abstracts',
            data_format,
            S.ArtifactAbstracts,
            ('artifactid', 'abstract')
        )

        # ------------------------------------------------------------
        # Joins
        #
        # JOIN artifacts a
        # JOIN artifact_abstracts ab
        # LEFT JOIN artifact_authorlists al
        # ------------------------------------------------------------

        rows = (
            au
            .join(
                a,
                left_on='artifactid',
                right_on='id',
                how='inner'
            )
            .join(
                ab,
                on='artifactid',
                how='inner'
            )
            .join(
                al,
                on='artifactid',
                how='left'
            )
        )

        # ------------------------------------------------------------
        # extractyear(a.date) = 2010
        # ------------------------------------------------------------

        rows = rows.filter(
            pl.col('date')
            .map_elements(
                self.scalar_udfs.extractyear,
                return_dtype=pl.Int64
            )
            == 2010
        )

        # ------------------------------------------------------------
        # blockkey(au.fullname, au.affiliation)
        #
        # COALESCE(al.authorlist, '[]')
        # ------------------------------------------------------------

        rows = rows.with_columns(
            pl.struct([
                'fullname',
                'affiliation'
            ])
            .map_elements(
                lambda r: self.scalar_udfs.blockkey(
                    r['fullname'],
                    r['affiliation']
                ),
                return_dtype=pl.String
            )
            .alias('bkey'),

            pl.col('authorlist')
            .fill_null('[]')
            .alias('coauthors')
        )

        # ------------------------------------------------------------
        # jsoncount(COALESCE(al.authorlist, '[]')) < 5
        #
        # frequentterms(
        #     stem(
        #         filterstopwords(
        #             keywords(ab.abstract)
        #         )
        #     ),
        #     10
        # )
        # ------------------------------------------------------------

        rows = (
            rows
            .with_columns(
                pl.col('coauthors')
                .map_elements(
                    self.scalar_udfs.jsoncount,
                    return_dtype=pl.Int64
                )
                .alias('author_count'),

                pl.col('abstract')
                .map_elements(
                    lambda value: self.scalar_udfs.frequentterms(
                        self.scalar_udfs.stem(
                            self.scalar_udfs.filterstopwords(
                                self.scalar_udfs.keywords(value)
                            )
                        ),
                        10
                    ),
                    return_dtype=pl.String
                )
                .alias('topic_terms')
            )
            .filter(
                pl.col('author_count') < 5
            )
        )

        # ------------------------------------------------------------
        # Exact input schema expected by resolveauthors
        # ------------------------------------------------------------

        rows = (
            rows
            .select([
                'artifactid',
                'bkey',
                'fullname',
                'affiliation',
                'coauthors',
                'topic_terms',
                'date'
            ])
            .rename({
                'artifactid': 'artifact_id',
                'fullname': 'raw_name',
                'affiliation': 'raw_affil',
                'date': 'event_date'
            })
            .collect()
        )

        # ------------------------------------------------------------
        # resolveauthors(...)
        # ------------------------------------------------------------

        return self.table_udfs.resolveauthors(
            rows,
            'sentence-transformers/all-MiniLM-L6-v2',
            'cpu'
        )
