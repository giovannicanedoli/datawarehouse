-- 1. Create Staging Tables
CREATE TABLE IF NOT EXISTS staging_global_threats (
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
    unified_industry TEXT
);

CREATE TABLE IF NOT EXISTS staging_net_crime (
    country TEXT,
    year INT,
    complaints INT,
    losses BIGINT
);

CREATE TABLE IF NOT EXISTS staging_breaches (
    id TEXT,
    entity TEXT,
    year TEXT,
    records TEXT,
    organization_type TEXT,
    method TEXT,
    unified_attack_category TEXT,
    unified_industry TEXT
);

-- 2. Load Data into Staging
COPY staging_global_threats 
FROM '/data/Global_Cybersecurity_Threats_unified.csv' 
WITH (FORMAT csv, HEADER true);

COPY staging_net_crime 
FROM '/data/LossFromNetCrime_unified.csv' 
WITH (FORMAT csv, HEADER true);

COPY staging_breaches 
FROM '/data/organization_data_breaches_unified.csv' 
WITH (FORMAT csv, HEADER true);

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
    attack_vector TEXT,
    vulnerability_type TEXT,
    unified_category TEXT
);

CREATE TABLE IF NOT EXISTS defense_dimension (
    defense_id SERIAL PRIMARY KEY,
    defense_mechanism TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS entity_dimension (
    entity_id SERIAL PRIMARY KEY,
    entity_name TEXT,
    industry TEXT,
    org_type TEXT,
    stolen_records INT
);

CREATE TABLE IF NOT EXISTS cyber_security_attack (
    geo_id INT,
    attack_id INT,
    defense_id INT,
    entity_id INT,
    time_id INT,
    PRIMARY KEY (geo_id, attack_id, defense_id, entity_id, time_id),
    affected_users BIGINT,
    financial_loss BIGINT,
    complaints INT,
    records_lost BIGINT,
    resolution_time_hours INT,
    FOREIGN KEY (geo_id) REFERENCES geography_dimension(geo_id),
    FOREIGN KEY (attack_id) REFERENCES attack_dimension(attack_id),
    FOREIGN KEY (defense_id) REFERENCES defense_dimension(defense_id),
    FOREIGN KEY (entity_id) REFERENCES entity_dimension(entity_id),
    FOREIGN KEY (time_id) REFERENCES time_dimension(time_id)
);

-- 4. Populate Dimensions
INSERT INTO time_dimension (year)
SELECT year FROM (
    SELECT DISTINCT year FROM staging_global_threats
    UNION
    SELECT DISTINCT year FROM staging_net_crime
) AS unique_years
ORDER BY year;

INSERT INTO geography_dimension (country)
SELECT DISTINCT country 
FROM staging_net_crime;

INSERT INTO geography_dimension (country)
SELECT DISTINCT country 
FROM staging_global_threats
ON CONFLICT DO NOTHING;

INSERT INTO attack_dimension (attack_type, attack_source, vulnerability_type, unified_category)
SELECT DISTINCT attack_type, attack_source, vulnerability_type, unified_attack_category
FROM staging_global_threats;

INSERT INTO attack_dimension (attack_type, unified_category)
SELECT DISTINCT method, unified_attack_category
FROM staging_breaches;

INSERT INTO defense_dimension (defense_mechanism)
SELECT DISTINCT defense_mechanism FROM staging_global_threats;

INSERT INTO entity_dimension (entity_name, industry, org_type)
SELECT DISTINCT entity, unified_industry, organization_type 
FROM staging_breaches
ON CONFLICT DO NOTHING;

-- 5. Populate Fact Table
INSERT INTO cyber_security_attack (time_id, geo_id, attack_id, defense_id, affected_users, resolution_time_hours)
SELECT 
    t.time_id,
    g.geo_id,
    a.attack_id,
    d.defense_id,
    s.affected_users,
    s.resolution_time_hours
FROM staging_global_threats s
JOIN time_dimension t ON s.year = t.year
JOIN geography_dimension g ON s.country = g.country
LEFT JOIN attack_dimension a ON s.attack_type = a.attack_type
LEFT JOIN defense_dimension d ON s.defense_mechanism = d.defense_mechanism;

INSERT INTO cyber_security_attack (time_id, geo_id, complaints, financial_loss)
SELECT 
    t.time_id,
    g.geo_id,
    s.complaints,
    s.losses
FROM staging_net_crime s
JOIN time_dimension t ON s.year = t.year
JOIN geography_dimension g ON s.country = g.country;

INSERT INTO cyber_security_attack (time_id, entity_id, attack_id, records_lost)
SELECT 
    t.time_id,
    e.entity_id,
    a.attack_id,
    CAST(NULLIF(regexp_replace(records, '[^0-9]', '', 'g'), '') AS BIGINT)
FROM staging_breaches s
JOIN time_dimension t ON CAST(s.year AS INT) = t.year
JOIN entity_dimension e ON s.entity = e.entity_name
LEFT JOIN attack_dimension a ON s.method = a.attack_type
WHERE s.year ~ '^\d+$';
