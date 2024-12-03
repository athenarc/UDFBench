SELECT artifacts.id, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                            select  * from extractkeys
                            ((select record,'publicationdoi','fundinginfo' from xmlparser
                            ((select column1,'publication' from file_q13('crossref.xml','text')))
                            ))
                            
                       ) xx
             ) AS crossref, artifacts
WHERE publicationdoi =artifacts.id
AND crossref.projectid NOT IN 
     (
      SELECT extractcode(fundingstring) as projectid 
      FROM projects_artifacts, projects ,artifacts
      WHERE projects_artifacts.artifactid = artifacts.id 
                     and projects.id =  projects_artifacts.projectid 
     )

;