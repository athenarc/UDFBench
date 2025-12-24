import utils

class Q17(utils.PandasQueryBase):
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
            table_udf_path=udf_paths['table_udf_path'],
        )

    def __exec__(
        self,
        dataset_path: str,
        data_format: utils.SupportedDataFormat,
        _: str
    ):
        stem = self.scalar_udfs.stem
        log_10 = self.scalar_udfs.log_10
        filterstopwords = self.scalar_udfs.filterstopwords
        keywords = self.scalar_udfs.keywords
        lowerize = self.scalar_udfs.lowerize
        strsplitv = self.table_udfs.strsplitv
        jgroupordered = self.table_udfs.jgroupordered

        ArtifactAbstracts = self.schemas.ArtifactAbstracts
        artifact_abstracts = self.__read_df__(
            dataset_path, 'artifact_abstracts',
            [
                ArtifactAbstracts.artifactid,
                ArtifactAbstracts.abstract,
            ],
            data_format
        )
        # nunique skips NaNs by default
        total_docid = artifact_abstracts[ArtifactAbstracts.artifactid].nunique()

        abstracts_stem = artifact_abstracts.loc[
            artifact_abstracts[ArtifactAbstracts.abstract].notna()
        ].apply(lambda r: (
            r[ArtifactAbstracts.artifactid],
            stem(filterstopwords(keywords(lowerize(r[ArtifactAbstracts.abstract]))))
        ), axis=1, result_type='expand')
        abstracts_stem.columns = ('docid', 'abstract')

        split_abstracts = abstracts_stem.loc[
            abstracts_stem['abstract'].notna()
        ]
        del artifact_abstracts, abstracts_stem
        split_abstracts = self.pd.concat((i for i in split_abstracts.apply(
            lambda r: self.pd.merge(
                self.pd.Series(r['docid'], name='docid'),
                self.pd.Series(strsplitv(r['abstract']), name='term'),
                how='cross'
            ), axis=1,
        )))
        split_abstracts.reset_index(drop=True, inplace=True)
        
        jgroup_data = (
            split_abstracts.groupby(['term', 'docid'])
                .size().reset_index(name='count')
        )
        del split_abstracts
        jgroup_data['tf'] = (
            jgroup_data['count'] / 
            jgroup_data.groupby('docid')['count'].transform('sum')
        )
        del jgroup_data['count']
        jg = jgroupordered(
            jgroup_data,
            order_by_col='term',
            count_col='docid'
        )
        
        jg['tfidf'] = jg.loc[:, ['jscount', 'tf']].apply(
            lambda r: (
                r['tf'] * (
                    log_10(
                        total_docid * 1.0 / (1.0 + r['jscount'])
                    ) + 1.0
                )
            ),
            axis=1
        )
        return jg.loc[:, ['docid', 'term', 'tfidf']]
