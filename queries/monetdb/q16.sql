WITH pairs(pubid, pubdate, projectstart, projectend, 
           funder, class, projectid, authorpair) as 
    
(
    SELECT pubid, pubdate, projectstart, projectend, 
           funder, fclass as class, projectid, authorpair
    FROM combinations((
            SELECT 
                pubid, pubdate, projectstart, projectend,funder,class,projectid, authorlist, 2
            FROM 
                (
                select artifact_authorlists.artifactid as pubid, artifacts.date as pubdate, projects.startdate as projectstart,  projects.enddate as projectend,
                extractfunder(projects.fundingstring) AS funder, 
                extractclass(projects.fundingstring) AS class,
                extractid(projects.fundingstring) AS projectid,
                jsort(jsortvalues(removeshortterms(lowerize(artifact_authorlists.authorlist)))) as authorlist
                from
                 projects, projects_artifacts, artifacts,artifact_authorlists  
                 where projects.id = projects_artifacts.projectid and projects_artifacts.artifactid = artifact_authorlists.artifactid and projects_artifacts.artifactid=artifacts.id 
                 and jsoncount(authorlist)<7 
                ) x 

        )) AS xx 
) 
SELECT funder, class, projectid,
  SUM(CASE WHEN cleandate(pubdate) between pstartcleaned and pendcleaned 
      THEN 1 ELSE NULL END) AS authors_during,
  SUM(CASE WHEN cleandate(pubdate) < pstartcleaned 
      THEN 1 ELSE NULL END) AS authors_before,
  SUM(CASE WHEN cleandate(pubdate) > pendcleaned 
      THEN 1 ELSE NULL END) AS authors_after
FROM (
    SELECT  projectpairs.funder, projectpairs.class, 
            projectpairs.projectid,
            cleandate(projectpairs.projectstart) AS pstartcleaned, 
            cleandate(projectpairs.projectend) AS pendcleaned, 
            pairs.authorpair, 
            pairs.pubdate   
    FROM 
        (
          SELECT * FROM pairs 
          WHERE projectid IS NOT NULL 
        ) AS projectpairs, pairs 
    WHERE projectpairs.authorpair = pairs.authorpair
) AS xx
GROUP BY funder, class, projectid;