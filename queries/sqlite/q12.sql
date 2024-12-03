SELECT artifactid, add_noise(count(*)) AS views 
FROM views_stats 
WHERE cleandate(date) >= strftime('%Y-%m-%d %H:%M:%S', 'now', '-18 months') 
GROUP BY artifactid 
ORDER BY views desc 
LIMIT 10;
