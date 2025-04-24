\COPY artifacts FROM 'artifacts.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY artifact_abstracts FROM 'artifact_abstracts.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY artifact_authorlists FROM 'artifact_authorlists.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY artifact_authors FROM 'artifact_authors.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY artifact_charges FROM 'artifact_charges.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY artifact_citations FROM 'artifact_citations.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY projects FROM 'projects.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY projects_artifacts FROM 'projects_artifacts.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY project_artifactcount FROM 'project_artifactcount.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
\COPY views_stats FROM 'views_stats.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);


create index projectsidx on projects(id,fundingstring);
create index projects_artifactsidx on projects_artifacts(projectid,artifactid);
create index projects_artifactsidx2 on projects_artifacts(artifactid);
create index artifactsidx on artifacts(id,date);
create unique index artifactsidx2 on artifacts(id);

create index artifact_abstractsidx on artifact_abstracts(md5(abstract),artifactid);

create unique index artifact_authorlistsidx on artifact_authorlists(md5(authorlist),artifactid)  where jsoncount(authorlist)<7;
create unique index artifact_authorlistsidx2 on artifact_authorlists(md5(authorlist),artifactid)  where jsoncount(authorlist)<=50;
