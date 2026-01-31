--ROLL UP QUERY: aggregating losses and complaints of a country over all years
SELECT g.country, SUM(cs.losses) as total_losses, SUM(cs.complaints) as total_complaints
FROM cyber_security_attack cs
JOIN geography_dimension g ON cs.geo_id = g.geo_id
GROUP BY g.country; 

WITH RegionalStats AS (
    -- Primo livello: Aggreghiamo i dati per Continente, Nazione e Anno
    SELECT 
        g.continent,
        g.country,
        t.year,
        SUM(cs.losses) as yearly_losses,
        SUM(SUM(cs.losses)) OVER (PARTITION BY g.country ORDER BY t.year) as cumulative_country_losses
    FROM cyber_security_attack cs
    JOIN geography_dimension g ON cs.geo_id = g.geo_id
    JOIN time_dimension t ON cs.time_id = t.time_id
    GROUP BY g.continent, g.country, t.year
),
ContinentTotals AS (
    -- Secondo livello: Calcoliamo il totale per continente usando una Window Function
    SELECT 
        *,
        SUM(yearly_losses) OVER (PARTITION BY continent) as total_continent_losses,
        RANK() OVER (PARTITION BY continent ORDER BY yearly_losses DESC) as country_rank_in_continent
    FROM RegionalStats
)
-- Risultato finale: Analisi comparativa
SELECT 
    continent,
    country,
    year,
    yearly_losses,
    cumulative_country_losses,
    ROUND((yearly_losses::numeric / NULLIF(total_continent_losses, 0)) * 100, 2) as percent_impact_on_continent
FROM ContinentTotals
WHERE country_rank_in_continent <= 5 -- Filtriamo solo le prime 5 nazioni per continente
ORDER BY continent, yearly_losses DESC;


-- DRILL-DOWN: Analisi della perdita record per Continente -> Industria -> Metodo di Attacco
SELECT 
    g.continent,
    e.industry,
    a.attack_type,
    SUM(cs.records_lost) as total_records_lost,
    COUNT(*) as number_of_incidents
FROM cyber_security_attack cs
JOIN geography_dimension g ON cs.geo_id = g.geo_id
JOIN entity_dimension e ON cs.entity_id = e.entity_id
JOIN attack_dimension a ON cs.attack_id = a.attack_id
WHERE cs.records_lost IS NOT NULL
GROUP BY g.continent, e.industry, a.attack_type
ORDER BY g.continent, total_records_lost DESC;



-- PIVOTING: Totale perdite economiche per Anno (Righe) e Continente (Colonne)
SELECT 
    t.year,
    SUM(cs.losses) FILTER (WHERE g.continent = 'Europe') as losses_europe,
    SUM(cs.losses) FILTER (WHERE g.continent = 'North America') as losses_north_america,
    SUM(cs.losses) FILTER (WHERE g.continent = 'Asia') as losses_asia,
    SUM(cs.losses) as global_total
FROM cyber_security_attack cs
JOIN time_dimension t ON cs.time_id = t.time_id
JOIN geography_dimension g ON cs.geo_id = g.geo_id
GROUP BY t.year
ORDER BY t.year;


-- SLICE AND DICE: Analisi mirata su "Healthcare" e "Finance" (Dice) nel periodo Post-Pandemia (Slice)
SELECT 
    g.country,
    e.industry,
    d.defense_mechanism,
    AVG(cs.resolution_time_hours) as avg_res_time,
    SUM(cs.affected_users) as total_victims
FROM cyber_security_attack cs
JOIN geography_dimension g ON cs.geo_id = g.geo_id
JOIN entity_dimension e ON cs.entity_id = e.entity_id
JOIN time_dimension t ON cs.time_id = t.time_id
JOIN defense_dimension d ON cs.defense_id = d.defense_id
WHERE t.pandemic_era = 'Post-Pandemic' -- Slice
  AND e.industry IN ('Healthcare', 'Finance') -- Dice
GROUP BY g.country, e.industry, d.defense_mechanism
HAVING SUM(cs.affected_users) > 1000
ORDER BY avg_res_time DESC;


-- BONUS: Defense Efficiency Index
WITH GlobalAvg AS (
    SELECT AVG(resolution_time_hours) as global_avg_time FROM cyber_security_attack
)
SELECT 
    d.defense_mechanism,
    COUNT(cs.geo_id) as times_deployed,
    ROUND(AVG(cs.resolution_time_hours), 2) as avg_defense_res_time,
    ROUND(
        (1 - (AVG(cs.resolution_time_hours) / (SELECT global_avg_time FROM GlobalAvg))) * 100, 
    2) as efficiency_score_percentage
FROM cyber_security_attack cs
JOIN defense_dimension d ON cs.defense_id = d.defense_id
WHERE cs.resolution_time_hours > 0
GROUP BY d.defense_mechanism
ORDER BY efficiency_score_percentage DESC;