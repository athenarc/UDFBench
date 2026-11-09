SELECT result.arxivid, result.pubmedid, result.similarity
FROM unnest(
    aggregate_top(
        'SELECT arxivid, pubmedid, similarity
         FROM (
             SELECT arxivid,
                    pubmedid,
                    deep_cosine(
                        deep_embed(arxiv_abstract, ''sentence-transformers/all-MiniLM-L6-v2'', ''cpu''),
                        deep_embed(pubmed_abstract, ''sentence-transformers/all-MiniLM-L6-v2'', ''cpu'')
                    ) AS similarity,
                    5
             FROM (SELECT tt.column0 AS arxivid, tt.column1 AS arxiv_abstract
                   FROM (SELECT unnest(file_q18(''arxiv.csv'', ''csv'')) AS tt)) arxiv,
                  (SELECT t.id AS pubmedid, t.abstract AS pubmed_abstract
                   FROM (SELECT unnest(file_q18b(''pubmed.txt'', ''json'')) AS t)) pubmed
         ) scored',
        'arxivid',
        'similarity',
        5
    )
) AS result;
