select * from (SELECT res.arxivid, res.pubmedid, res.similarity from (select unnest(aggregate_top('SELECT arxivid,
             pubmedid,
             deep_similarity_score(arxivterms,
                           pmcterms, ''sentence-transformers/all-MiniLM-L6-v2'', ''cuda'')
             AS similarity from (select * from (
       SELECT tt.column0 as arxivid,
                    tt.column1   AS arxivterms
             FROM (select  unnest(file_q18(''arxiv.csv'', ''csv'')) as tt  ) ),
              (SELECT t.id as pubmedid,
                   t.abstract AS pmcterms
             FROM (select  unnest(file_q18b(''pubmed.txt'', ''json'')) as t) ))'
             ,'arxivid','similarity',5)) as res) ) ;
