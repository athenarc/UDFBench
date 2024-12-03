
Select aggregate_count(pairs) from (Select combinations(clean(authorlist), 2) as pairs from  artifact_authorlists where jsoncount(authorlist)<=50 ) ;
