select aggregate_count(authorpairs) from  combinations(
    TABLE(select clean(authorlist) from 
    (select * from artifact_authorlists where jsoncount(authorlist)<=50) zz),2);