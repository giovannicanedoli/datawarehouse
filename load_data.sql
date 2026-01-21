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
    west_or_east TEXT
);

CREATE TEMP TABLE IF NOT EXISTS staging_net_crime (
    country TEXT,
    year INT,
    complaints INT,
    losses BIGINT,
    continent TEXT,     
    nation_wealth TEXT, 
    west_or_east TEXT 
);

CREATE TEMP TABLE IF NOT EXISTS staging_breaches (
    id TEXT,
    entity TEXT,
    year TEXT,
    records TEXT,
    organization_type TEXT,
    method TEXT,
    unified_attack_category TEXT,
    unified_industry TEXT
    -- Note: No country/continent here based on your previous error
);

-- 2. Load Data into Staging
COPY staging_global_threats FROM '/data/Global_Cybersecurity_Threats_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_net_crime FROM '/data/LossFromNetCrime_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_breaches FROM '/data/organization_data_breaches_unified.csv' WITH (FORMAT csv, HEADER true);

-- 3. Create Dimensions
CREATE TABLE IF NOT EXISTS time_dimension (
    time_id SERIAL PRIMARY KEY,
    year INT
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
    stolen_records TEXT
);

-- 4. Create Fact Table
CREATE TABLE IF NOT EXISTS cyber_security_attack (
    geo_id INT NOT NULL,
    attack_id INT NOT NULL,
    defense_id INT NOT NULL,
    entity_id INT NOT NULL,
    time_id INT NOT NULL,
    affected_users BIGINT,
    financial_loss BIGINT,
    complaints INT,
    records_lost TEXT,
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
FROM staging_global_threats;

INSERT INTO time_dimension (year)
SELECT DISTINCT year FROM staging_global_threats
UNION
SELECT DISTINCT CAST(NULLIF(year, '') AS INT) FROM staging_breaches WHERE year ~ '^\d+$'
UNION
SELECT DISTINCT year FROM staging_net_crime;

INSERT INTO attack_dimension(attack_type, attack_source, vulnerability_type, unified_category)
SELECT DISTINCT attack_type, attack_source, vulnerability_type, unified_attack_category
FROM staging_global_threats;

INSERT INTO defense_dimension (defense_mechanism)
SELECT DISTINCT defense_mechanism FROM staging_global_threats WHERE defense_mechanism IS NOT NULL;

INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records)
SELECT DISTINCT 
    entity, 
    unified_industry, 
    organization_type,
    records
FROM staging_breaches;

-- 6. Insert Fact Table (Joins)
-- First, insert default records for NULL defense and entity dimensions
INSERT INTO defense_dimension (defense_mechanism) VALUES ('Unknown') ON CONFLICT DO NOTHING;
INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records) VALUES ('Unknown', 'Unknown', 'Unknown', 'Unknown') ON CONFLICT DO NOTHING;

-- Insert fact table with aggregation and defaults for missing dimensions
INSERT INTO cyber_security_attack (geo_id, attack_id, defense_id, entity_id, time_id, affected_users, financial_loss, resolution_time_hours)
SELECT 
    g.geo_id, 
    a.attack_id, 
    COALESCE(d.defense_id, (SELECT defense_id FROM defense_dimension WHERE defense_mechanism = 'Unknown' LIMIT 1)),
    COALESCE(e.entity_id, (SELECT entity_id FROM entity_dimension WHERE entity_name = 'Unknown' LIMIT 1)),
    t.time_id, 
    SUM(s.affected_users), 
    0, 
    AVG(s.resolution_time_hours)::INT
FROM staging_global_threats s
JOIN geography_dimension g ON s.country = g.country
JOIN attack_dimension a    ON s.attack_type = a.attack_type
JOIN time_dimension t      ON s.year = t.year
LEFT JOIN defense_dimension d ON s.defense_mechanism = d.defense_mechanism
LEFT JOIN entity_dimension e ON s.target_industry = e.industry
GROUP BY g.geo_id, a.attack_id, d.defense_id, e.entity_id, t.time_id;   --one row per data


DO $$
BEGIN
    RAISE NOTICE '✓ Fact table insert completed at %', NOW();
    RAISE NOTICE '✓ Total rows in cyber_security_attack: %', (SELECT COUNT(*) FROM cyber_security_attack);
END $$;

-- -- Update Fact table with Net Crime data (use attack_id=1 as default for aggregated net crime data)
-- INSERT INTO cyber_security_attack (geo_id, attack_id, time_id, financial_loss, complaints)
-- SELECT g.geo_id, 1, t.time_id, s.losses, s.complaints
-- FROM staging_net_crime s
-- JOIN geography_dimension g ON s.country = g.country 
-- JOIN time_dimension t      ON s.year = t.year
-- ON CONFLICT (geo_id, attack_id, time_id) DO UPDATE
-- SET financial_loss = EXCLUDED.financial_loss, complaints = EXCLUDED.complaints;