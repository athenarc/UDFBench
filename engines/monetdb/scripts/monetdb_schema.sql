


CREATE TABLE artifacts(id STRING , title STRING, publisher STRING, journal STRING, date STRING, "year" INTEGER, access_mode STRING, embargo_end_date STRING, delayed BOOLEAN, authors INTEGER, source STRING, abstract BOOLEAN, "type" STRING, peer_reviewed BOOLEAN, green BOOLEAN, gold BOOLEAN);
CREATE TABLE artifact_charges(artifactid STRING PRIMARY KEY, amount FLOAT, currency STRING);
CREATE TABLE artifact_abstracts(artifactid STRING NOT NULL, abstract STRING);
CREATE TABLE artifact_authorlists(artifactid STRING PRIMARY KEY, authorlist STRING);
CREATE TABLE artifact_authors(artifactid STRING NOT NULL, affiliation STRING, fullname STRING, "name" STRING, surname STRING, rank INTEGER, authorid STRING);
CREATE TABLE artifact_citations(artifactid STRING PRIMARY KEY, target STRING, citcount BIGINT);
CREATE TABLE projects(id STRING PRIMARY KEY, acronym STRING, title STRING, funder STRING, fundingstring STRING, funding_lvl0 STRING, funding_lvl1 STRING, funding_lvl2 STRING, ec39 STRING, "type" STRING, startdate STRING, enddate STRING, start_year INTEGER, end_year INTEGER, duration INTEGER, haspubs STRING, numpubs BIGINT, daysforlastpub INTEGER, delayedpubs BIGINT, callidentifier STRING, code STRING, totalcost FLOAT, fundedamount FLOAT, currency STRING);
CREATE TABLE projects_artifacts(projectid STRING NOT NULL, artifactid STRING NOT NULL, provenance STRING);
CREATE TABLE project_artifactcount(projectid STRING PRIMARY KEY, publications BIGINT, datasets BIGINT, software BIGINT, other BIGINT);
CREATE TABLE views_stats(date STRING NOT NULL, artifactid STRING NOT NULL, source STRING, repository_id STRING, count BIGINT);




