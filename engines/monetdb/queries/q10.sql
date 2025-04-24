select * from kmeans_iterative((select * from (
    select id, "type", sum(fundedamount) as amount ,5 from (
        select artifacts.id as id , artifacts.type as "type", converttoeuro(projects.fundedamount, projects.currency) as fundedamount
        from  artifacts, projects, projects_artifacts
        where artifacts.id = projects_artifacts.artifactid and projects_artifacts.projectid = projects.id and projects.fundedamount>0.0
        ) as X group by id, "type"
   ) aa)) xxx ;
