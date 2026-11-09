-- Q27: Deep-learning table UDF for author identity resolution.
-- The list returned by resolveauthors is expanded with UNNEST.
SELECT resolved.person_id, resolved.artifact_id, resolved.raw_affil, resolved.event_date
FROM unnest(resolveauthors(
    'SELECT au.artifactid AS artifact_id,
            blockkey(au.fullname, au.affiliation) AS bkey,
            au.fullname AS raw_name,
            au.affiliation AS raw_affil,
            COALESCE(al.authorlist, ''[]'') AS coauthors,
            frequentterms(stem(filterstopwords(keywords(ab.abstract))), 10) AS topic_terms,
            a.date AS event_date
     FROM artifact_authors au
     JOIN artifacts a ON a.id = au.artifactid
     JOIN artifact_abstracts ab ON ab.artifactid = au.artifactid
     LEFT JOIN artifact_authorlists al ON al.artifactid = au.artifactid
     WHERE au.rank = 1
       AND extractyear(a.date) = 2010
       AND jsoncount(COALESCE(al.authorlist, ''[]'')) < 5',
    'sentence-transformers/all-MiniLM-L6-v2',
    'cpu'
)) AS result(resolved);
