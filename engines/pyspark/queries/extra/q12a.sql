WITH random_values AS (
    SELECT
        artifactid,
        COUNT(*)
 AS base_views,
        RAND() AS r
    FROM views_stats
    WHERE TO_TIMESTAMP(date, 'yyyy/MM/dd') >= (CURRENT_TIMESTAMP - INTERVAL 24 MONTH)
    GROUP BY artifactid
)
SELECT
    artifactid,
     base_views + (SQRT(-2 * LOG(r)) * COS(2 * 3.141592653589793 * (r + 0.5)) * 2) AS views
FROM random_values
ORDER BY views DESC
LIMIT 10;