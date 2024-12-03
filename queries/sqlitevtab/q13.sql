
SELECT publicationdoi, crossref.projectid
FROM (
           SELECT c1 as publicationdoi, extractprojectid(c2) as projectid
            FROM (
                        SELECT  * from jsonparser('id','publicationdoi','fundinginfo', "query: select * from fileparse('crossref.txt','text')")
                       ) AS T
             ) AS crossref
;