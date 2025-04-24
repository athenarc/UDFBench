
SELECT artifacts.id, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        select xx.key1 as publicationdoi, xx.key2 as fundinginfo from (
                             select extractkeys(rec,'publicationdoi','fundinginfo')  as xx from (SELECT  unnest(xmlparser(x.line,'publication')) as rec
                from(select unnest(file_q15('crossref.xml','text')) as x))
                 
                        )
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


