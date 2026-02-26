-- RECONSTRUCTING BASIC CUBE

SELECT *
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN time_dimension t ON f.time_id = t.time_id
JOIN attack_dimension a ON f.attack_id = a.attack_id
JOIN defense_dimension d ON f.defense_id = d.defense_id
JOIN entity_dimension e ON f.entity_id = e.entity_id

SELECT *
FROM fact_net_crime_stats f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN time_dimension t ON f.time_id = t.time_id

-- ROLL UP

SELECT g.continent,
t.year, 
SUM(f.affected_users) as total_affected_users
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN time_dimension t ON f.time_id = t.time_id
GROUP BY g.continent, t.year
ORDER BY g.continent, t.year;


-- DRILL DOWN

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


-- DRILL ACROSS

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


-- PIVOT

SELECT
   a.unified_category,
   COUNT(CASE WHEN g.west_or_east = 'Western' THEN 1 END) AS attacks_west,
   COUNT(CASE WHEN g.west_or_east = 'Eastern' THEN 1 END) AS attacks_east
FROM fact_cyber_incidents f
JOIN geography_dimension g ON f.geo_id = g.geo_id
JOIN attack_dimension a ON f.attack_id = a.attack_id
GROUP BY a.unified_category
ORDER BY a.unified_category;




-- SLICE AND DICE

SELECT
    g.continent,
    a.attack_type,
    SUM(f.records_lost) as total_records_lost,
    COUNT(f.entity_id) as total_entities
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


-- GET ECONOMIC INSIGHTS ON ATTACKS

WITH AttackGivenMalwareAndGeo AS (
    SELECT 
        f.geo_id, 
        f.time_id, 
        f.attack_id,
        SUM(f.records_lost) as total_records_lost,
        SUM(f.affected_users) as total_affected_users
    FROM fact_cyber_incidents f
    JOIN attack_dimension ad ON f.attack_id = ad.attack_id
    WHERE f.records_lost IS NOT NULL
    GROUP BY f.geo_id, f.time_id, f.attack_id, ad.unified_category
),
AttackGivenMalware AS (
    SELECT 
        f.attack_id,
        f.time_id, 
        SUM(f.records_lost) as malware_records_lost
    FROM fact_cyber_incidents f
    JOIN attack_dimension a ON f.attack_id = a.attack_id 
    WHERE f.records_lost IS NOT NULL AND a.attack_type <> 'Unknown'
    GROUP BY f.attack_id, f.time_id
)
SELECT 
    gd.continent,
    gd.country,
    t.year,
    a.attack_type,
    amg.total_records_lost AS total_stolen_entries,
    agm.malware_records_lost AS total_lost_due_to_malware_type
    ncs.total_financial_losses AS annual_lost,
    CAST(amg.total_records_lost AS FLOAT) / NULLIF(ncs.total_financial_losses, 0) AS danger_ratio
FROM AttackGivenMalwareAndGeo amg
JOIN AttackGivenMalware agm ON amg.attack_id = agm.attack_id AND amg.time_id = agm.time_id 
JOIN fact_net_crime_stats ncs ON amg.geo_id = ncs.geo_id AND amg.time_id = ncs.time_id
JOIN geography_dimension gd ON amg.geo_id = gd.geo_id
JOIN time_dimension t ON agm.time_id = t.time_id
JOIN attack_dimension a ON agm.attack_id = a.attack_id
ORDER BY danger_ratio DESC;


-- GET ECONOMIC INSIGHTS ON DEFENSES

WITH DefenseMechanismAndGeo AS (
    SELECT 
        f.geo_id, 
        f.time_id, 
        f.defense_id,
        SUM(f.resolution_time_hours) as resolution_hours_by_geo_id,
        SUM(f.records_lost) as records_lost_by_geo_id
    FROM fact_cyber_incidents f
    JOIN defense_dimension d ON f.defense_id = d.defense_id
    WHERE f.resolution_time_hours IS NOT NULL AND d.defense_mechanism <> 'Unknown'
    GROUP BY f.geo_id, f.time_id, f.defense_id
),
DefenseMechanism AS (
    SELECT 
        f.defense_id,
        f.time_id, 
        SUM(f.records_lost) as total_records_lost,
        SUM(f.resolution_time_hours) as total_defense_hours
    FROM fact_cyber_incidents f
    JOIN defense_dimension d ON f.defense_id = d.defense_id
    WHERE f.resolution_time_hours IS NOT NULL AND d.defense_mechanism <> 'Unknown'
    GROUP BY f.defense_id, f.time_id
)
SELECT 
    gd.continent,
    gd.country,
    t.year,
    dd.defense_mechanism,
    dmg.resolution_hours_by_geo_id,
    dmg.records_lost_by_geo_id,
    dm.total_records_lost,
    dm.total_defense_hours,
    ncs.total_financial_losses AS annual_lost,
    CAST(ncs.total_financial_losses AS FLOAT) / NULLIF(dmg.resolution_hours_by_geo_id, 0) AS financial_defense_rate_per_hour

FROM DefenseMechanismAndGeo dmg
JOIN DefenseMechanism dm ON dmg.defense_id = dm.defense_id AND dmg.time_id = dm.time_id
JOIN fact_net_crime_stats ncs ON dmg.geo_id = ncs.geo_id AND dmg.time_id = ncs.time_id
JOIN geography_dimension gd ON dmg.geo_id = gd.geo_id
JOIN time_dimension t ON dmg.time_id = t.time_id
JOIN defense_dimension dd ON dmg.defense_id = dd.defense_id
ORDER BY financial_defense_rate_per_hour DESC;


-- STATISTICAL ANALYSIS

WITH continent_financial_statistics AS (
    SELECT 
        g.continent,
        t.year,
        COUNT(*) AS total_crime_reports,
        AVG(f.total_financial_losses) AS mean_financial_loss,
        STDDEV(f.total_financial_losses) AS std_dev_financial_loss,
        VARIANCE(f.total_financial_losses) AS variance_financial_loss
    FROM fact_net_crime_stats f
    JOIN geography_dimension g ON f.geo_id = g.geo_id
    JOIN time_dimension t ON f.time_id = t.time_id
    WHERE f.resolution_time_hours IS NOT NULL
    GROUP BY g.continent, t.year
),
incident_impacts AS (
    SELECT 
        g.continent,
        t.year,
        COUNT(*) AS total_incidents,
        AVG(fci.records_lost) AS mean_records_lost,
        STDDEV(fci.records_lost) AS std_dev_records_lost,
        VARIANCE(fci.records_lost) AS variance_records_lost,
        AVG(fci.resolution_time_hours) AS mean_resolution_time
    FROM fact_cyber_incidents fci
    JOIN geography_dimension g ON fci.geo_id = g.geo_id
    JOIN time_dimension t ON fci.time_id = t.time_id
    WHERE f.resolution_time_hours IS NOT NULL
    GROUP BY g.continent, t.year
)
SELECT 
    rf.year,
    rf.continent,
    rf.total_crime_reports,
    rf.mean_financial_loss,
    rf.std_dev_financial_loss,
    ii.total_incidents,
    ii.mean_records_lost,
    ii.std_dev_records_lost,
    ii.mean_resolution_time
FROM continent_financial_statistics st
JOIN incident_impacts ii 
ON st.year = ii.year AND st.continent = ii.continent
ORDER BY st.year DESC, st.mean_financial_loss DESC;