SELECT
    group_column1 AS arxivid,
    group_column2 AS pubmedid,
    top_s
FROM aggregate_top(
    TABLE(
        SELECT
            arxivid,
            pubmedid,
            deep_similarity_score(
                arxiv_abstract,
                pubmed_abstract,
                'sentence-transformers/all-MiniLM-L6-v2',
                'cuda'
            ) AS similarity
        FROM
            (
                SELECT
                    column1 AS arxivid,
                    column2 AS arxiv_abstract
                FROM file_q18('arxiv.csv', 'csv')
            ) arxiv
        CROSS JOIN
            (
                SELECT
                    column1 AS pubmedid,
                    column2 AS pubmed_abstract
                FROM file_q18('pubmed.txt', 'json')
            ) pubmed
    ),
    5,
    'arxivid',
    'pubmedid',
    'similarity'
);
