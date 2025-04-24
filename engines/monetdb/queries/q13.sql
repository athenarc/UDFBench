SELECT publicationdoi, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        select * from  jsonparse
                        ((select column1  ,'publicationdoi','fundinginfo' 
                        from file_q13('crossref.txt','text') xx)) z 
                       ) AS T
             ) AS crossref
;