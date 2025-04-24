create temp table author_pairs as 
WITH author_pairs AS (
        SELECT authorpair, pubdate
        FROM (
            SELECT * FROM combinations((
                 select  date,
                 jsort(jsortvalues(removeshortterms(lowerize(authorlist)))) as authors, 2
                 from artifacts, artifact_authorlists
            WHERE artifact_authorlists.artifactid = artifacts.id 
              AND jsoncount(authorlist) < 7 
                     
            
            ))
        ) AS X WHERE authorpair NOT LIKE '%[''""'',%'
      AND authorpair NOT LIKE '%, ''""'']%'
    ) 
    SELECT authorpair, pubdate FROM author_pairs on commit preserve rows;
    
SELECT * FROM logistic_regression_recursive_train((
    SELECT authorpair, STR_TO_DATE(pubdate, '%Y-%m-%d') AS date, 'authorpair', 'date',  100, 1e-4  FROM author_pairs

)) AS t;