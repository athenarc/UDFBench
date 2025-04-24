explain (analyse,buffers)
SELECT publicationdoi, crossref.projectid 
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        SELECT  * from jsonparse('select * from file(''crossref.txt'',''text'')
                                f(id text)','id','publicationdoi','fundinginfo') f(publicationdoi text, fundinginfo text)
                       ) AS T
             ) AS crossref
;
