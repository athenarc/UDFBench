select t.* from (select unnest(pivot_udf('SELECT * FROM (
    SELECT pr.projectid AS _pid, r.type AS result_type
    FROM (select id,type from artifacts) r
    JOIN projects_artifacts pr ON r.id = pr.artifactid) AS SourceTable','_pid','result_type','size') ) as t)
    AS PivotTable;
