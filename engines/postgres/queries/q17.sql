explain (analyse,buffers) WITH total_docid AS (
    SELECT COUNT(DISTINCT artifactid)  as doc_count FROM artifact_abstracts
    
)  
select docid,term,(tf*(log_10(((SELECT max(doc_count) FROM total_docid)*1.0)/(1.0+jcount))+1.0)) as tfidf 
from  JGROUPORDERED('select  term,docid,(1.0*count(*))/(1.0* sum(count(*)) OVER (PARTITION BY docid)) AS tf 
from(
    
        select docid, Strsplitv(abstract) as term from(
            select  artifactid as docid, stem(filterstopwords(keywords(lowerize(abstract)))) as abstract from artifact_abstracts
        )
     )
    group by term,docid','term','docid') 
;
