
WiTH total_docid AS (
    SELECT COUNT(DISTINCT artifactid)  as doc_count FROM artifact_abstracts
    
) 
SELECT
    docid,
    term, 
    (tf * (log_10((cast(((SELECT max(doc_count) FROM total_docid) * 1.0) as float)) / (1.0 + jcount))+ 1.0)) AS tfidf
FROM
    (
        SELECT docid, term, tf, jcount
        FROM JGROUPORDERED(
            (SELECT
                term,
                docid,
                 cast((1.0*count(*)) as float)/(1.0* sum(count(*)) OVER (PARTITION BY docid)) AS tf ,
                'term' AS order_by_col,
                'docid' AS count_col
            FROM
                (

                    SELECT docid, term
                    FROM STRSPLITV((SELECT artifactid as docid, stem(filterstopwords(keywords(lowerize(abstract)))) AS abstract FROM artifact_abstracts)) AS xx
                ) AS xxx
            GROUP BY term, docid
            )
        ) AS xxxx
    ) AS b;