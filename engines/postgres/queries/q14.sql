explain (analyse,buffers)
with aa (artifactid, authorid, affiliation, rank, authoridvalue, affiliationvalue ) as       
( select artifactid, authorid, affiliation, rank,                   
         jsonparse(authorid, 'value') as authoridvalue,                  
         jsonparse(affiliation, 'value') as affiliationvalue from artifact_authors        
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
      (aa.authorid, cleandate(a.date)) in 
          (select authorid, aggregate_max(cleandate(a.date)) as max_date 
          from artifact_authors as aa, artifacts as a            
              where aa.rank = 1 and aa.artifactid = a.id            
          group by authorid);
