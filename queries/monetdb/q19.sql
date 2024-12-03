SELECT * FROM PIVOT(
    (SELECT pid, result_type,'pid'as group_by_column,'result_type' as pivot_column, 'size'  as aggregate_function FROM 
    ( SELECT pr.projectid AS pid, r.type AS result_type 
    FROM artifacts r 
    JOIN projects_artifacts pr ON r.id = pr.artifactid) AS SourceTable)
) AS PivotTable;