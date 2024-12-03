select artifactid, add_noise(COUNT(*)) AS views fROM views_stats 
WHERE CAST(cleandate(date) AS TIMESTAMP)  >= NOW - INTERVAL '18' MONTH
group by artifactid 
ORDER BY views desc
LIMIT 10;
