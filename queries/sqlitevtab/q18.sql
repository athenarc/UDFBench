
select arxivid, aggregate_top(5,similarity,pubmedid, similarity) from (select * from (SELECT arxivid, 
             pubmedid, 
             JACCARD(arxivterms, pmcterms) 
             AS similarity from (select * from (SELECT c1 as arxivid,
                    jpack(
                    FREQUENTTERMS(
                    STEM(
                    FILTERSTOPWORDS(
                    keywords(
                    c2
                    ))), 10)) 
                    AS arxivterms
             FROM (SELECT * FROM file('arxiv.csv', 'csv') WHERE C2 IS NOT NULL))),
              (SELECT c1 as pubmedid, 
                    jpack(
                    FREQUENTTERMS(
                    STEM(
                    FILTERSTOPWORDS(
                    keywords(
                   c2
                   ))), 10)) 
                   AS pmcterms
             FROM ( SELECT * FROM file('pubmed.txt', 'json') WHERE C2 IS NOT NULL)))
             )
             group by arxivid;
