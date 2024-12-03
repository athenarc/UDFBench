
select arxivid, aggregate_top(5,similarity,pubmedid, similarity) from (select * from (SELECT arxivid, 
             pubmedid, 
             JACCARD_v2(arxivterms, pmcterms) 
             AS similarity from (select * from (SELECT c1 as arxivid,
                    jpack_v2(
                    FREQUENTTERMS_v2(
                    STEM_v2(
                    filterstopwords_v2(
                    keywords_v2(
                    c2
                    ))), 10)) 
                    AS arxivterms
             FROM (SELECT * FROM fileparse('arxiv.csv', 'csv') WHERE C2 IS NOT NULL))),
              (SELECT c1 as pubmedid, 
                    jpack_v2(
                    FREQUENTTERMS_v2(
                    STEM_v2(
                    filterstopwords_v2(
                    keywords_v2(
                   c2
                   ))), 10)) 
                   AS pmcterms
             FROM ( SELECT * FROM fileparse('pubmed.txt', 'json') WHERE C2 IS NOT NULL)))
             )
             group by arxivid;
