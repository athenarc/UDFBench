
SELECT id, projectid
FROM (
       SELECT * FROM (   select publicationdoi, extractprojectid(fundinginfo) as projectid from (select key1 as publicationdoi, key2 as fundinginfo from (select ( extractkeys(c1,'publicationdoi','fundinginfo'))
from xmlparser("publication","c1", "query: select * from file('crossref.xml','text')"))) ) as crossref, artifacts as A
WHERE crossref.publicationdoi=A.id
AND crossref.projectid NOT IN
     (
      SELECT extractcode(projects.fundingstring) as projectid
      FROM projects_artifacts, projects, artifacts
      WHERE projects_artifacts.artifactid = artifacts.id
                     and projects.id =  projects_artifacts.projectid
     )
);


