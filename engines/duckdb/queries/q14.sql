with aa (artifactid, authorid, affiliation, rank, authoridvalue, affiliationvalue ) as       
( select artifactid, authorid, affiliation, rank,                   
         jsonparse_q14(authorid, 'value') as authoridvalue,                  
         jsonparse_q14(affiliation, 'value') as affiliationvalue from artifact_authors        
where affiliation is not null 
      and affiliation <> '[]' 
      and authorid is not null 
      and authorid <> '[]' ) 
select aa.authoridvalue, aa.affiliationvalue 
from aa, artifacts a, projects_artifacts pr, projects p 
where aa.rank = 1 and 
      aa.artifactid = a.id and 
      p.id = pr.projectid and 
      pr.artifactid = a.id and 
      p.funder = 'European Commission' and 
      ((aa.authorid, cleandate(a.date))) in 
          (select (x.grp, x.max ) from(select  unnest(aggregate_max('select cleandate(a.date) as date ,authorid  as grp
    FROM artifact_authors AS aa
    JOIN artifacts AS a ON aa.artifactid = a.id
    WHERE aa.rank = 1','date','grp')) AS x));