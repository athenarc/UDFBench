


CREATE TABLE artifacts(id TEXT PRIMARY KEY, title TEXT, publisher TEXT, journal TEXT, date TEXT, "year" INTEGER, access_mode TEXT, embargo_end_date TEXT, delayed BOOLEAN, authors INTEGER, source TEXT, abstract BOOLEAN, "type" TEXT, peer_reviewed BOOLEAN, green BOOLEAN, gold BOOLEAN);
CREATE TABLE artifact_charges(artifactid TEXT PRIMARY KEY, amount FLOAT, currency TEXT);
CREATE TABLE artifact_abstracts(artifactid TEXT NOT NULL, abstract TEXT);
CREATE TABLE artifact_authorlists(artifactid TEXT PRIMARY KEY, authorlist TEXT);
CREATE TABLE artifact_authors(artifactid TEXT NOT NULL, affiliation TEXT, fullname TEXT, "name" TEXT, surname TEXT, rank INTEGER, authorid TEXT);
CREATE TABLE artifact_citations(artifactid TEXT PRIMARY KEY, target TEXT, citcount BIGINT);
CREATE TABLE projects(id TEXT PRIMARY KEY, acronym TEXT, title TEXT, funder TEXT, fundingstring TEXT, funding_lvl0 TEXT, funding_lvl1 TEXT, funding_lvl2 TEXT, ec39 TEXT, "type" TEXT, startdate TEXT, enddate TEXT, start_year INTEGER, end_year INTEGER, duration INTEGER, haspubs TEXT, numpubs BIGINT, daysforlastpub INTEGER, delayedpubs BIGINT, callidentifier TEXT, code TEXT, totalcost FLOAT, fundedamount FLOAT, currency TEXT);
CREATE TABLE projects_artifacts(projectid TEXT NOT NULL, artifactid TEXT NOT NULL, provenance TEXT);
CREATE TABLE project_artifactcount(projectid TEXT PRIMARY KEY, publications BIGINT, datasets BIGINT, software BIGINT, other BIGINT);
CREATE TABLE views_stats(date TEXT NOT NULL, artifactid TEXT NOT NULL, source TEXT, repository_id TEXT, count BIGINT);


CREATE EXTENSION plpython3u;


