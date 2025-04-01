select artifactid, addnoise(COUNT(*)) AS views fROM views_stats 
WHERE TO_TIMESTAMP(cleandate(date), 'yyyy/MM/dd')  >= (CURRENT_TIMESTAMP - INTERVAL 24 MONTH)
group by artifactid 
ORDER BY views desc
LIMIT 10;