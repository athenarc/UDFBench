SELECT
    funder,
    dl_embed_agg(
        abstract,
        'sentence-transformers/all-MiniLM-L6-v2',
        'cuda'
    ) AS funder_embedding
FROM (
    SELECT
        extractfunder(p.fundingstring) AS funder,
        ab.abstract AS abstract
    FROM projects p
    JOIN projects_artifacts pa
        ON pa.projectid = p.id
    JOIN artifacts a
        ON a.id = pa.artifactid
    JOIN artifact_abstracts ab
        ON ab.artifactid = a.id
    WHERE extractyear(a.date)>2020
) t
GROUP BY funder;
