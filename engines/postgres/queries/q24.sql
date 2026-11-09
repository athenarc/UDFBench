-- Q24: Deep-learning abstract similarity with one fused scalar UDF.
-- Change the device argument to 'cuda' for GPU execution.

explain (analyse,buffers)
select *
from aggregate_top(
    'SELECT arxivid,
            pubmedid,
            deep_similarity_score(
                arxiv_abstract,
                pubmed_abstract,
                ''sentence-transformers/all-MiniLM-L6-v2'',
                ''cuda''
            ) AS similarity
     FROM (SELECT pubmed_df as arxivid, abstract as arxiv_abstract
           FROM file(''arxiv.csv'', ''csv'') f1(pubmed_df text, abstract text)) arxiv,
          (SELECT pubmedid, abstract as pubmed_abstract
           FROM file(''pubmed.txt'', ''json'') f2(pubmedid text, abstract text)) pubmed',
    5,
    'arxivid',
    'similarity'
) ranked(arxivid text, pubmedid text, similarity double precision);
