SELECT id, title,
       dlpredict_citations(CAST(author_count AS INT), CAST(COALESCE(citcount, 0) AS BIGINT), extractyear(date), 'cuda') AS predicted_impact,
       COALESCE(citcount, 0) AS current_citations
FROM (
  SELECT a.id, a.title, a.date, ab.abstract, ac.citcount,
         COUNT(DISTINCT au.authorid) AS author_count
  FROM artifacts a
  JOIN artifact_abstracts ab ON ab.artifactid = a.id
  JOIN artifact_authors au ON au.artifactid = a.id
  JOIN projects_artifacts pa ON pa.artifactid = a.id
  JOIN projects p ON p.id = pa.projectid
  LEFT JOIN artifact_citations ac ON ac.artifactid = a.id
  WHERE extractfunder(p.fundingstring) = 'FP7'
  GROUP BY a.id, a.title, a.date, ab.abstract, ac.citcount
) AS fofo
ORDER BY predicted_impact DESC
LIMIT 20;
