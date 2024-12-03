explain (analyse,buffers) 
select * from kmeans_recursive(
    'select id, type, sum(fundedamount) as fundedamount from (
            select artifacts.id as id, artifacts.type as type, converttoeuro(projects.fundedamount, projects.currency) as fundedamount
            from  artifacts, projects, projects_artifacts
            where artifacts.id = projects_artifacts.artifactid and projects_artifacts.projectid = projects.id and projects.fundedamount>0.0) group by id, type','type','fundedamount','id',5) 
            f(clusterid int, id text,type text,points double precision) ;
