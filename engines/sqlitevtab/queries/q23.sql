SELECT arxivid,
       aggregate_top(5, similarity, pubmedid, similarity)
FROM (
    SELECT arxiv.c1 AS arxivid,
           pubmed.c1 AS pubmedid,
           deep_cosine(
               deep_embed(arxiv.c2, 'sentence-transformers/all-MiniLM-L6-v2', 'cpu'),
               deep_embed(pubmed.c2, 'sentence-transformers/all-MiniLM-L6-v2', 'cpu')
           ) AS similarity,
           5
    FROM file('arxiv.csv', 'csv') AS arxiv,
         file('pubmed.txt', 'json') AS pubmed
) AS scored
GROUP BY arxivid;
