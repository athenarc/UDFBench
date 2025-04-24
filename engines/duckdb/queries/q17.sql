WITH total_docid AS (
    SELECT COUNT(DISTINCT artifactid)  as doc_count FROM artifact_abstracts
    
)  
select x.docid,x.term,(x.tf*(log_10(((SELECT max(doc_count) FROM total_docid)*1.0)/(1.0+x.jcount))+1.0)) as tfidf 
from (select unnest(JGROUPORDERED('
select  term,docid,(1.0*count(*))/(1.0* sum(count(*)) OVER (PARTITION BY docid)) AS tf 
from(
    
        select docid, unnest(strsplitv(abstract).term) as term from(
            select  artifactid as docid, stem(filterstopwords(keywords(lowerize(abstract)))) as abstract from artifact_abstracts
        )
     )
    group by term,docid','term','docid') ) as x) 
;
