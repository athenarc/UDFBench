
copy  into  artifacts from 'artifacts.csv'  USING DELIMITERS ',',E'\n', '\"'  NO ESCAPE NULL as '';
copy  into  artifact_abstracts FROM 'artifact_abstracts.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  artifact_authorlists FROM 'artifact_authorlists.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  artifact_authors FROM 'artifact_authors.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  artifact_charges from 'artifact_charges.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  artifact_citations FROM 'artifact_citations.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  projects FROM 'projects.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  projects_artifacts FROM 'projects_artifacts.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  project_artifactcount FROM 'project_artifactcount.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
copy  into  views_stats FROM 'views_stats.csv' USING DELIMITERS ',',E'\n', '\"' NO ESCAPE NULL as '';
