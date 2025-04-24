
INSERT INTO projects_artifacts 
SELECT  crossref.projectid, publicationdoi, 'crossref'
FROM (
           SELECT c1 as publicationdoi, extractprojectid(c2) as projectid
            FROM (
                        SELECT  * from jsonparse('id','publicationdoi','fundinginfo', "query: select * from file('data.txt','text')")
                       ) AS T
             ) AS crossref;


