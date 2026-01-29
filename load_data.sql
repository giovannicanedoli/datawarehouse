-- 1. Create Staging Tables
CREATE TEMP TABLE IF NOT EXISTS staging_global_threats (
    country TEXT,
    year INT,
    attack_type TEXT,
    target_industry TEXT,
    affected_users INT,
    attack_source TEXT,
    vulnerability_type TEXT,
    defense_mechanism TEXT,
    resolution_time_hours INT,
    unified_attack_category TEXT,
    unified_industry TEXT,
    continent TEXT,     
    nation_wealth TEXT, 
    west_or_east TEXT,
    pandemic_era TEXT,
    is_leap_year BOOLEAN
);

CREATE TEMP TABLE IF NOT EXISTS staging_net_crime (
    country TEXT,
    year INT,
    complaints BIGINT,
    losses BIGINT,
    continent TEXT,     
    nation_wealth TEXT, 
    west_or_east TEXT,
    pandemic_era TEXT,
    is_leap_year BOOLEAN 
);

CREATE TEMP TABLE IF NOT EXISTS staging_breaches (
    id TEXT,
    entity TEXT,
    year INT,
    records BIGINT,
    organization_type TEXT,
    method TEXT,
    unified_attack_category TEXT,
    unified_industry TEXT,
    pandemic_era TEXT,
    is_leap_year BOOLEAN
    -- Note: No country/continent here based on your previous error
);

-- 2. Load Data into Staging
COPY staging_global_threats FROM '/data/Global_Cybersecurity_Threats_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_net_crime FROM '/data/LossFromNetCrime_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_breaches FROM '/data/organization_data_breaches_unified.csv' WITH (FORMAT csv, HEADER true);

-- 3. Create Dimensions
CREATE TABLE IF NOT EXISTS time_dimension (
    time_id SERIAL PRIMARY KEY,
    year INT,
    pandemic_era TEXT,
    is_leap_year BOOLEAN
);

CREATE TABLE IF NOT EXISTS geography_dimension (
    geo_id SERIAL PRIMARY KEY,
    country TEXT,
    continent TEXT,
    nation_wealth TEXT,
    west_or_east TEXT
);

CREATE TABLE IF NOT EXISTS attack_dimension (
    attack_id SERIAL PRIMARY KEY,
    attack_type TEXT,
    attack_source TEXT,
    vulnerability_type TEXT,
    unified_category TEXT
);

CREATE TABLE IF NOT EXISTS defense_dimension (
    defense_id SERIAL PRIMARY KEY,
    defense_mechanism TEXT
);

CREATE TABLE IF NOT EXISTS entity_dimension (
    entity_id SERIAL PRIMARY KEY,
    entity_name TEXT,
    industry TEXT,
    org_type TEXT,
    stolen_records BIGINT
);

-- 4. Create Fact Table
CREATE TABLE IF NOT EXISTS cyber_security_attack (
    geo_id INT NOT NULL,
    attack_id INT NOT NULL,
    defense_id INT NOT NULL,
    entity_id INT NOT NULL,
    time_id INT NOT NULL,
    complaints BIGINT,
    losses BIGINT,
    affected_users BIGINT,
    records_lost BIGINT,
    resolution_time_hours INT,
    PRIMARY KEY (geo_id, attack_id, time_id, defense_id, entity_id),
    FOREIGN KEY (geo_id) REFERENCES geography_dimension(geo_id),
    FOREIGN KEY (attack_id) REFERENCES attack_dimension(attack_id),
    FOREIGN KEY (defense_id) REFERENCES defense_dimension(defense_id),
    FOREIGN KEY (entity_id) REFERENCES entity_dimension(entity_id),
    FOREIGN KEY (time_id) REFERENCES time_dimension(time_id)
);

-- 5. Insert Dimensions (Using DISTINCT to avoid duplicates)
INSERT INTO geography_dimension (country, continent, nation_wealth, west_or_east)
SELECT DISTINCT country, continent, nation_wealth, west_or_east
FROM staging_global_threats
UNION 
SELECT DISTINCT country, continent, nation_wealth, west_or_east
FROM staging_net_crime;

INSERT INTO time_dimension (year, pandemic_era, is_leap_year)
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_global_threats
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_breaches
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_net_crime;

INSERT INTO attack_dimension (attack_type, attack_source, vulnerability_type, unified_category)
SELECT DISTINCT attack_type, attack_source, vulnerability_type, unified_attack_category
FROM staging_global_threats s
WHERE NOT EXISTS (
    SELECT 1 FROM attack_dimension a 
    WHERE a.attack_type = s.attack_type 
      AND a.attack_source = s.attack_source
      AND a.vulnerability_type = s.vulnerability_type
);

INSERT INTO defense_dimension (defense_mechanism)
SELECT DISTINCT defense_mechanism FROM staging_global_threats WHERE defense_mechanism IS NOT NULL;

INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records)
SELECT DISTINCT ON (entity)
    entity,
    unified_industry, 
    organization_type,
    records
FROM staging_breaches s;




WITH summary_net_crime AS (
    SELECT 
        year, 
        country, 
        SUM(complaints) as total_complaints,
        SUM(losses) as total_losses
    FROM staging_net_crime
    GROUP BY year, country
)
INSERT INTO cyber_security_attack (
    geo_id, attack_id, defense_id, entity_id, time_id, 
    complaints, losses, affected_users, resolution_time_hours, records_lost
)
SELECT DISTINCT 
    g.geo_id, 
    a.attack_id,
    d.defense_id, 
    e.entity_id,
    t.time_id, 
    n.total_complaints, 
    n.total_losses,
    s.affected_users,
    s.resolution_time_hours,
    b.records
FROM staging_global_threats s
JOIN geography_dimension g ON s.country = g.country
JOIN attack_dimension a    ON s.attack_type = a.attack_type
JOIN time_dimension t      ON s.year = t.year
JOIN defense_dimension d   ON s.defense_mechanism = d.defense_mechanism
LEFT JOIN summary_net_crime n ON s.country = n.country AND s.year = n.year
LEFT JOIN staging_breaches b ON s.year = b.year 
    AND s.unified_industry = b.unified_industry  -- Join on industry match
JOIN entity_dimension e ON b.entity = e.entity_name
ON CONFLICT (geo_id, attack_id, time_id, defense_id, entity_id) DO NOTHING;

DO $$
BEGIN
    RAISE NOTICE 'Fact table insert completed at % ✓', NOW();
    RAISE NOTICE 'Total rows in cyber_security_attack: % ✓', (SELECT COUNT(*) FROM cyber_security_attack);
END $$;
