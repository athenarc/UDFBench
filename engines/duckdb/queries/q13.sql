SELECT publicationdoi, crossref.projectid 
FROM (
           SELECT xx.publicationdoi, extractprojectid(xx.fundinginfo) as projectid
            FROM (
                SELECT  jsonparse(x.line,'publicationdoi','fundinginfo') as xx
                from(select unnest(file_q13('crossref.txt','text')) as x)
                       ) AS T
             ) AS crossref
;
