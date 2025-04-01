SELECT artifactid, addnoise(count(*)) AS views
FROM views_stats 
WHERE cleandate(date)::TIMESTAMP::TIMESTAMP WITH TIME ZONE  >= (NOW() - INTERVAL 24 MONTH)
GROUP BY artifactid
ORDER BY views desc
LIMIT 10;