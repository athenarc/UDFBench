


CREATE TABLE artifacts(id VARCHAR PRIMARY KEY, title VARCHAR, publisher VARCHAR, journal VARCHAR, date VARCHAR, "year" INTEGER, access_mode VARCHAR, embargo_end_date VARCHAR, delayed BOOLEAN, authors INTEGER, source VARCHAR, abstract BOOLEAN, "type" VARCHAR, peer_reviewed BOOLEAN, green BOOLEAN, gold BOOLEAN);
CREATE TABLE artifact_charges(artifactid VARCHAR PRIMARY KEY, amount FLOAT, currency VARCHAR);
CREATE TABLE artifact_abstracts(artifactid VARCHAR NOT NULL, abstract VARCHAR);
CREATE TABLE artifact_authorlists(artifactid VARCHAR PRIMARY KEY, authorlist VARCHAR);
CREATE TABLE artifact_authors(artifactid VARCHAR NOT NULL, affiliation VARCHAR, fullname VARCHAR, "name" VARCHAR, surname VARCHAR, rank INTEGER, authorid VARCHAR);
CREATE TABLE artifact_citations(artifactid VARCHAR PRIMARY KEY, target VARCHAR, citcount BIGINT);
CREATE TABLE projects(id VARCHAR PRIMARY KEY, acronym VARCHAR, title VARCHAR, funder VARCHAR, fundingstring VARCHAR, funding_lvl0 VARCHAR, funding_lvl1 VARCHAR, funding_lvl2 VARCHAR, ec39 VARCHAR, "type" VARCHAR, startdate VARCHAR, enddate VARCHAR, start_year INTEGER, end_year INTEGER, duration INTEGER, haspubs VARCHAR, numpubs BIGINT, daysforlastpub INTEGER, delayedpubs BIGINT, callidentifier VARCHAR, code VARCHAR, totalcost FLOAT, fundedamount FLOAT, currency VARCHAR);
CREATE TABLE projects_artifacts(projectid VARCHAR NOT NULL, artifactid VARCHAR NOT NULL, provenance VARCHAR);
CREATE TABLE project_artifactcount(projectid VARCHAR PRIMARY KEY, publications BIGINT, datasets BIGINT, software BIGINT, other BIGINT);
CREATE TABLE views_stats(date VARCHAR NOT NULL, artifactid VARCHAR NOT NULL, source VARCHAR, repository_id VARCHAR, count BIGINT);




