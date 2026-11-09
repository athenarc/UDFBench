SELECT group_column1 AS arxivid, group_column2 AS pubmedid, top_s
FROM aggregate_top(
    TABLE(
        SELECT arxivid, pubmedid, similarity
        FROM (
            SELECT arxivid,
                   pubmedid,
                   deep_cosine(
                       deep_embed(arxiv_abstract, 'sentence-transformers/all-MiniLM-L6-v2', 'cpu'),
                       deep_embed(pubmed_abstract, 'sentence-transformers/all-MiniLM-L6-v2', 'cpu')
                   ) AS similarity,
                   5
            FROM (
                SELECT column1 AS arxivid, column2 AS arxiv_abstract
                FROM file_q18('/data/hdd1/users/jfouf/udfbench_extended/UDFBench/dataset/files/large/arxiv.csv', 'csv')
            ) arxiv,
            (
                SELECT column1 AS pubmedid, column2 AS pubmed_abstract
                FROM file_q18('/data/hdd1/users/jfouf/udfbench_extended/UDFBench/dataset/files/large/pubmed.txt', 'json')
            ) pubmed
        ) scored
    ),
    5,
    'arxivid',
    'pubmedid',
    'similarity'
);
