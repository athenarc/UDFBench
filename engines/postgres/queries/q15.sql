
explain (analyse,buffers)
SELECT artifacts.id, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        select key1 as publicationdoi, key2 as fundinginfo from (select ( extractkeys(rec,'publicationdoi','fundinginfo')).* 
                        from xmlparser('select * from file(''crossref.xml'',''text'') f(id text)','publication','id') f(rec text))
                       ) 
                       AS T
             ) AS crossref, artifacts
WHERE publicationdoi =artifacts.id
AND crossref.projectid NOT IN 
     (
      SELECT extractcode(projects.fundingstring) as projectid 
      FROM projects_artifacts, projects
      WHERE projects_artifacts.artifactid = artifacts.id 
                     and projects.id =  projects_artifacts.projectid   
     )
;