explain (analyse,buffers) 
select * from 
PIVOT('SELECT * FROM (
    SELECT pr.projectid AS pid, r.type AS result_type
    FROM (select id,type from artifacts) r
    JOIN projects_artifacts pr ON r.id = pr.artifactid) AS SourceTable','pid','result_type','size') 
    AS PivotTable(pid text, datasets int, other int, publications int, software int);
