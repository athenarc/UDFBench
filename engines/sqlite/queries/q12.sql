SELECT artifactid, addnoise(count(*)) AS views 
FROM views_stats 
WHERE cleandate(date) >= strftime('%Y/%m/%d %H:%M:%S', 'now', '-24 months') 
GROUP BY artifactid 
ORDER BY views desc 
LIMIT 10;
