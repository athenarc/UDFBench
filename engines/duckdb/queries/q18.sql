select * from (SELECT res.arxivid, res.pubmedid, res.similarity from (select unnest(aggregate_top('SELECT arxivid, 
             pubmedid, 
             JACCARD_udf(arxivterms, 
                           pmcterms) 
             AS similarity from (select * from (
       SELECT tt.column0 as arxivid,
                    JPACK(
                    FREQUENTTERMS(
                    STEM(
                    FILTERSTOPWORDS(
                    KEYWORDS(
                    tt.column1
                    ))), 10)) 
                    AS arxivterms
             FROM (select  unnest(file_q18(''arxiv.csv'', ''csv'')) as tt  ) ),
              (SELECT t.id as pubmedid, 
                   JPACK(
                   FREQUENTTERMS(
                   STEM(
                   FILTERSTOPWORDS(
                   KEYWORDS(
                   t.abstract
                   ))), 10)) 
                   AS pmcterms
             FROM (select  unnest(file_q18b(''pubmed.txt'', ''json'')) as t) ))'
             ,'arxivid','similarity',5)) as res) ) ;
