EXPLAIN (ANALYZE, BUFFERS)
SELECT a.id,
       a.title,
       dlpredict_citations(
           cast(COUNT(DISTINCT au.authorid) as integer),
           cast(COALESCE(ac.citcount, 0) as bigint),
           extractyear(a.date),
           cast('cuda' as text)
       ) AS predicted_impact,
       COALESCE(ac.citcount, 0) AS current_citations
FROM artifacts a
JOIN artifact_authors au ON au.artifactid = a.id
JOIN projects_artifacts pa ON pa.artifactid = a.id
JOIN projects p ON p.id = pa.projectid
LEFT JOIN artifact_citations ac ON ac.artifactid = a.id
WHERE extractfunder(p.fundingstring) = 'FP7'
GROUP BY a.id, a.title, a.date, ac.citcount
ORDER BY predicted_impact DESC
LIMIT 20;

