SELECT arxivid, pubmedid, similarity
FROM aggregate_top(
    'SELECT arxivid, pubmedid, similarity
     FROM (
         SELECT arxivid,
                pubmedid,
                deep_cosine(
                    deep_embed(arxiv_abstract, ''sentence-transformers/all-MiniLM-L6-v2'', ''cpu''),
                    deep_embed(pubmed_abstract, ''sentence-transformers/all-MiniLM-L6-v2'', ''cpu'')
                ) AS similarity,
                5
         FROM (SELECT column1 AS arxivid, column2 AS arxiv_abstract
               FROM file(''arxiv.csv'', ''csv'') f1(column1 text, column2 text)) arxiv,
              (SELECT column1 AS pubmedid, column2 AS pubmed_abstract
               FROM file(''pubmed.txt'', ''json'') f2(column1 text, column2 text)) pubmed
     ) scored',
    5,
    'arxivid',
    'similarity'
) ranked(arxivid text, pubmedid text, similarity double precision);
