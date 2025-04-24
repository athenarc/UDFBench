CREATE TABLE IF NOT EXISTS `artifacts` (
  `id` TEXT PRIMARY KEY NOT NULL,
  `title` TEXT,
  `publisher` TEXT,
  `journal` TEXT,
  `date` TEXT,
  `year` INTEGER,
  `access_mode` TEXT,
  `embargo_end_date` TEXT,
  `delayed` INTEGER,
  `authors` INTEGER,
  `source` TEXT,
  `abstract` INTEGER,
  `type` TEXT,
  `peer_reviewed` INTEGER,
  `green` INTEGER,
  `gold` INTEGER
);

CREATE TABLE IF NOT EXISTS `artifact_abstracts` (
  `artifactid` TEXT NOT NULL,
  `abstract` TEXT,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `artifact_authorlists` (
  `artifactid` TEXT PRIMARY KEY NOT NULL,
  `authorlist` TEXT,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `artifact_authors` (
  `artifactid` TEXT NOT NULL,
  `affiliation` TEXT,
  `fullname` TEXT,
  `name` TEXT,
  `surname` TEXT,
  `rank` INT,
  `authorid` TEXT,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `projects` (
  `id` TEXT PRIMARY KEY NOT NULL,
  `acronym` TEXT,
  `title` TEXT,
  `funder` TEXT,
  `fundingstring` TEXT,
  `funding_lvl0` TEXT,
  `funding_lvl1` TEXT,
  `funding_lvl2` TEXT,
  `ec39` TEXT,
  `type` TEXT,
  `startdate` TEXT,
  `enddate` TEXT,
  `start_year` INTEGER,
  `end_year` INTEGER,
  `duration` INTEGER,
  `haspubs` TEXT,
  `numpubs` INTEGER,
  `daysforlastpub` INTEGER,
  `delayedpubs` INTEGER,
  `callidentifier` TEXT,
  `code` TEXT,
  `totalcost` REAL,
  `fundedamount` REAL,
  `currency` TEXT
);

CREATE TABLE IF NOT EXISTS `project_artifactcount` (
  `projectid` TEXT PRIMARY KEY NOT NULL,
  `publications` INTEGER,
  `datasets` INTEGER,
  `software` INTEGER,
  `other` INTEGER,
  FOREIGN KEY (`projectid`) REFERENCES `projects` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `artifact_charges` (
  `artifactid` TEXT PRIMARY KEY NOT NULL,
  `amount` REAL,
  `currency` TEXT,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `artifact_citations` (
  `artifactid` TEXT PRIMARY KEY NOT NULL,
  `target` TEXT,
  `citcount` INTEGER,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `views_stats` (
  `date` TEXT NOT NULL,
  `artifactid` TEXT NOT NULL,
  `source` TEXT,
  `repository_id` TEXT,
  `count` INTEGER,
    FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS `projects_artifacts` (
  `projectid` TEXT NOT NULL,
  `artifactid` TEXT NOT NULL,
  `provenance` TEXT,
  PRIMARY KEY (`artifactid`, `projectid`),
  FOREIGN KEY (`projectid`) REFERENCES `projects` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY (`artifactid`) REFERENCES `artifacts` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
);
