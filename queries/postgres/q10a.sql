explain (analyse,buffers) 
SELECT * FROM logistic_regression_iterative_train(
    $$ 
    WITH author_pairs AS (
        SELECT authorpair, artifactid, date
        FROM ((
            SELECT artifact_authorlists.artifactid, 
                   TO_DATE(artifacts.date, 'YYYY-MM-DD') AS date,
                   combinations(jsort(jsortvalues(removeshortterms(lowerize(authorlist)))),2) AS authorpair
            FROM artifacts, artifact_authorlists
            WHERE artifact_authorlists.artifactid = artifacts.id 
              AND jsoncount(authorlist) < 7 
        )) WHERE authorpair NOT LIKE '%[''""'',%'
      AND authorpair NOT LIKE '%, ''""'']%'
    )
    SELECT authorpair, date FROM author_pairs
    $$,
    'authorpair', 
    'date', 
    100, 
    1e-4
) AS t;