INSERT INTO projects_artifacts 
SELECT  crossref.projectid, publicationdoi, 'crossref'
FROM (
           SELECT xx.publicationdoi, extractprojectid(xx.fundinginfo) as projectid
            FROM (
                SELECT  jsonparse(x.line,'publicationdoi','fundinginfo') as xx
                from(select unnest(file_q13('data.txt','text')) as x)
                       ) AS T
             ) AS crossref
;
