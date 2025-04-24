
select * from PIVOT('pid','result_type','size', 'query: SELECT * FROM (     SELECT pr.projectid AS pid, r.type AS result_type     FROM (select id,type from artifacts) r     JOIN projects_artifacts pr ON r.id = pr.artifactid) AS SourceTable');
