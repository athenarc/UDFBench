SELECT * FROM (
select group_column1 as arxivid, group_column2 as pubmedid, top_s from aggregate_top (TABLE(SELECT arxivid, 
             pubmedid, 
             JACCARD(arxivterms, 
                           pmcterms) 
             AS similarity
       FROM (SELECT arxivid,
                    JPACK(
                    FREQUENTTERMS(
                    STEM(
                    FILTERSTOPWORDS(
                    KEYWORDS(
                    abstract
                    ))), 10)) 
                    AS arxivterms
             FROM (select column1 as arxivid, column2 as abstract from file_q18('arxiv.csv', 'csv') ) xx ) xxx, 
           (SELECT pubmedid, 
                   JPACK(
                   FREQUENTTERMS(
                   STEM(
                   FILTERSTOPWORDS(
                   KEYWORDS(
                   abstract
                   ))), 10)) 
                   AS pmcterms
             FROM (select column1 as pubmedid, column2 as abstract from file_q18('pubmed.txt', 'json')) zz  )zzz),5,'arxivid','pubmedid','similarity') xxzz
 ) ;

