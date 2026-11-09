-- Q24: Deep-learning abstract similarity with one fused scalar UDF.
-- Change the device argument to 'cuda' for GPU execution.

select group_column1 as arxivid, group_column2 as pubmedid, top_s
from aggregate_top (
    (SELECT arxivid,
            pubmedid,
            deep_similarity_score(
                arxiv_abstract,
                pubmed_abstract,
                'sentence-transformers/all-MiniLM-L6-v2',
                'cuda'
            ) AS similarity,
            5
     FROM (SELECT column1 as arxivid, column2 as arxiv_abstract
           FROM file_q18('arxiv.csv', 'csv')) arxiv,
          (SELECT column1 as pubmedid, column2 as pubmed_abstract
           FROM file_q18('pubmed.txt', 'json')) pubmed
    )
) ranked;
