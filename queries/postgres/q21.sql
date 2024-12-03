
explain  (analyse,buffers)
INSERT INTO projects_artifacts 
SELECT  crossref.projectid, publicationdoi, 'crossref'
FROM (
           SELECT publicationdoi, extractprojectid(fundinginfo) as projectid
            FROM (
                        SELECT  * from jsonparse('select * from file(''data.txt'',''text'')
                                f(id text)','id','publicationdoi','fundinginfo') f(publicationdoi text, fundinginfo text)
                       ) AS T
             ) AS crossref
;