explain (analyse,buffers) 
SELECT artifactid, addnoise(count(*)) AS views
FROM views_stats 
WHERE cleandate(date)::timestamp with time zone  >= NOW() - INTERVAL '24 months'
GROUP BY artifactid
ORDER BY views desc
LIMIT 10;