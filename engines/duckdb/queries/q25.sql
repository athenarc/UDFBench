SELECT
    result.grp AS funder,
    result.embedding AS funder_embedding
FROM unnest(
    dl_embed_agg(
        'SELECT extractfunder(p.fundingstring) AS funder, ab.abstract
         FROM projects p
         JOIN projects_artifacts pa ON pa.projectid = p.id
         JOIN (
             SELECT id, date
             FROM artifacts
             WHERE extractyear(date) > 2020
         ) a ON a.id = pa.artifactid
         JOIN artifact_abstracts ab ON ab.artifactid = a.id',
        'abstract',
        'funder',
        'sentence-transformers/all-MiniLM-L6-v2',
        'cuda'
    )
) AS t(result);
