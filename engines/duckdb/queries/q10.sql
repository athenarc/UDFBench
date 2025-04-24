select res.* from (select unnest(kmeans_iterative(
    'select id, type, sum(fundedamount) as fundedamount from (
            select artifacts.id as id, artifacts.type as type, converttoeuro(projects.fundedamount, projects.currency) as fundedamount
            from  artifacts, projects, projects_artifacts
            where artifacts.id = projects_artifacts.artifactid and projects_artifacts.projectid = projects.id and projects.fundedamount>0.0) group by id, type',5,'type','fundedamount','id') 
) as res);
