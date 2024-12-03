

INSERT INTO projects_artifacts 
SELECT  crossref.projectid, publicationdoi, 'crossref'
FROM (
           SELECT c1 as publicationdoi, extractprojectid(c2) as projectid
            FROM (
                        SELECT  * from jsonparser('id','publicationdoi','fundinginfo', "query: select * from fileparse('data.txt','text')")
                       ) AS T
             ) AS crossref;

