SELECT artifacts.id, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                            select  * from extractkeys
                            (TABLE(select * from xmlparser
                            (TABLE(select column1 from file_q13('crossref.xml','text')),'publication')
                            ),'publicationdoi','fundinginfo' )
                            
                       ) xx
             ) AS crossref, artifacts
WHERE publicationdoi =artifacts.id
AND crossref.projectid NOT IN 
     (
      SELECT extractcode(fundingstring) as projectid 
      FROM projects_artifacts, projects
      WHERE projects_artifacts.artifactid = artifacts.id 
                     and projects.id =  projects_artifacts.projectid 
     )

;