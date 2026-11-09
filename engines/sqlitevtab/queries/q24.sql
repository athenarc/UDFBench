SELECT
    arxivid,
    aggregate_top(5, similarity, pubmedid, similarity)
FROM (
    SELECT
        arxiv.arxivid,
        pubmed.pubmedid,
        deep_similarity_score(
            arxiv.arxiv_abstract,
            pubmed.pubmed_abstract,
            'sentence-transformers/all-MiniLM-L6-v2',
            'cuda'
        ) AS similarity
    FROM (
        SELECT c1 AS arxivid, c2 AS arxiv_abstract
        FROM file('arxiv.csv', 'csv')
    ) AS arxiv
    CROSS JOIN (
        SELECT c1 AS pubmedid, c2 AS pubmed_abstract
        FROM file('pubmed.txt', 'json')
    ) AS pubmed
) AS scored
GROUP BY arxivid;
