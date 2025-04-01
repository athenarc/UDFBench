SELECT publicationdoi, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        select * from  jsonparse
                        (TABLE(select column1
                        from file_q13('crossref.txt','text')) ,'publicationdoi','fundinginfo' )
                       ) AS T
             ) AS crossref
;