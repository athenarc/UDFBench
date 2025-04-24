INSERT INTO projects_artifacts 
SELECT  crossref.projectid, publicationdoi, 'crossref'
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        select * from  jsonparse
                        ((select column1  ,'publicationdoi','fundinginfo' 
                        from file_q13('data.txt','text') xx)) z 
                       ) AS T
             ) AS crossref
;


