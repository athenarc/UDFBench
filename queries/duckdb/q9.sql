select aggregate_count('Select unnest(combinations(clean(authorlist), 2)) as pairs from  artifact_authorlists where jsoncount(authorlist)<=50 ','pairs') as aggregate_count;
