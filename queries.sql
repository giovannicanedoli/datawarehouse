-- 1 ROLL UP

SELECT g.continent,
t.year, 
SUM(f.affected_users) as total_affected_users
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN time_dimension t ON f.time_id = t.time_id
GROUP BY g.continent, t.year
ORDER BY g.continent, t.year;


-- 2 DRILL DOWN

SELECT
   g.country,
   a.unified_category,
   a.attack_type,
   SUM(f.records_lost) as total_records_lost
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN attack_dimension a ON f.attack_id = a.attack_id
WHERE g.continent = 'Europe'
GROUP BY g.country, a.unified_category, a.attack_type
ORDER BY total_records_lost DESC;


-- 3 DRILL ACROSS

WITH incident_metrics AS (
   SELECT
       time_id,
       SUM(records_lost) as total_records_lost
   FROM fact_cyber_incidents
   GROUP BY time_id
),
crime_stats_metrics AS (
   SELECT
       time_id,
       SUM(total_financial_losses) as total_financial_losses
   FROM fact_net_crime_stats
   GROUP BY time_id
)
SELECT
   t.year,
   im.total_records_lost,
   cs.total_financial_losses
FROM time_dimension t
LEFT JOIN incident_metrics im ON t.time_id = im.time_id
LEFT JOIN crime_stats_metrics cs ON t.time_id = cs.time_id
ORDER BY t.year;


-- 4 PIVOT

SELECT
   a.unified_category,
   COUNT(CASE WHEN g.west_or_east = 'Western' THEN 1 END) AS attacks_west,
   COUNT(CASE WHEN g.west_or_east = 'Eastern' THEN 1 END) AS attacks_east
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN attack_dimension a ON f.attack_id = a.attack_id
GROUP BY a.unified_category
ORDER BY a.unified_category;




-- Slice and dice

SELECT
    g.continent,
    a.attack_type,
    SUM(f.records_lost) as total_records_lost
    COUNT(f.entity_id) as total_incidents
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN attack_dimension a ON f.attack_id = a.attack_id
JOIN time_dimension t ON f.time_id = t.time_id
JOIN entity_dimension e ON f.entity_id = e.entity_id
WHERE
    t.year >= 2018
    AND e.industry = 'Healthcare'
    AND g.west_or_east = 'Western'
GROUP BY 
    g.continent,
    a.attack_type
ORDER BY
    g.continent,
    total_records_lost DESC;
