-- Create Staging Tables
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
    nation_welfare TEXT, 
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
    nation_welfare TEXT, 
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
    is_leap_year BOOLEAN,
    country TEXT,
    continent TEXT,
    nation_welfare TEXT, 
    west_or_east TEXT
);

-- Load data into staging tables
COPY staging_global_threats FROM '/data/Global_Cybersecurity_Threats_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_net_crime FROM '/data/LossFromNetCrime_unified.csv' WITH (FORMAT csv, HEADER true);
COPY staging_breaches FROM '/data/organization_data_breaches_unified.csv' WITH (FORMAT csv, HEADER true);

-- Create dimensions
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
    nation_welfare TEXT,
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
    defense_mechanism TEXT,
    vulnerability_type TEXT
);

CREATE TABLE IF NOT EXISTS entity_dimension (
    entity_id SERIAL PRIMARY KEY,
    entity_name TEXT,
    industry TEXT,
    org_type TEXT,
    stolen_records BIGINT
);

-- Create fact tables
CREATE TABLE IF NOT EXISTS fact_net_crime_stats (
    geo_id INT NOT NULL,
    time_id INT NOT NULL,

    total_complaints BIGINT,
    total_financial_losses BIGINT,


    PRIMARY KEY (geo_id, time_id),
    FOREIGN KEY (geo_id) REFERENCES geography_dimension(geo_id),
    FOREIGN KEY (time_id) REFERENCES time_dimension(time_id)
);

CREATE TABLE IF NOT EXISTS fact_cyber_incidents (    

    geo_id INT NOT NULL,
    time_id INT NOT NULL,
    attack_id INT NOT NULL,
    defense_id INT NOT NULL,
    entity_id INT NOT NULL,

    affected_users BIGINT,
    records_lost BIGINT,
    resolution_time_hours INT,
    


    PRIMARY KEY (geo_id, time_id, attack_id, defense_id, entity_id),
    FOREIGN KEY (geo_id) REFERENCES geography_dimension(geo_id),
    FOREIGN KEY (time_id) REFERENCES time_dimension(time_id),
    FOREIGN KEY (attack_id) REFERENCES attack_dimension(attack_id),
    FOREIGN KEY (defense_id) REFERENCES defense_dimension(defense_id),
    FOREIGN KEY (entity_id) REFERENCES entity_dimension(entity_id)
);

-- Insert Geography Dimension
INSERT INTO geography_dimension (country, continent, nation_welfare, west_or_east) 
SELECT DISTINCT country, continent, nation_welfare, west_or_east 
FROM staging_global_threats
UNION 
SELECT DISTINCT country, continent, nation_welfare, west_or_east 
FROM staging_net_crime
UNION
SELECT DISTINCT country, continent, nation_welfare, west_or_east
FROM staging_breaches;

-- Insert Time Dimension
INSERT INTO time_dimension (year, pandemic_era, is_leap_year)
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_global_threats
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_breaches
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_net_crime;

-- Insert Attack Dimension
INSERT INTO attack_dimension (attack_type, attack_source, vulnerability_type, unified_category)
SELECT DISTINCT attack_type, attack_source, vulnerability_type, unified_attack_category
FROM staging_global_threats s;

INSERT INTO attack_dimension (attack_type, attack_source, unified_category) 
VALUES ('Unknown', 'Unknown', 'Unknown');


-- Insert Defense Dimension
INSERT INTO defense_dimension (defense_mechanism, vulnerability_type)
SELECT DISTINCT defense_mechanism, vulnerability_type FROM staging_global_threats WHERE defense_mechanism IS NOT NULL;
INSERT INTO defense_dimension (defense_mechanism, vulnerability_type) 
VALUES ('Unknown', 'Unknown');

-- Insert Entity Dimension
INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records)
SELECT DISTINCT ON (entity)
    entity,
    unified_industry, 
    organization_type,
    records
FROM staging_breaches s;
INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records) 
VALUES ('Unknown', 'Unknown', 'Unknown', 0);

-- Insert Fact Cyber Incidents
INSERT INTO fact_cyber_incidents (
    geo_id, time_id, attack_id, defense_id, entity_id, 
    affected_users, resolution_time_hours, records_lost
)
SELECT DISTINCT ON (geo_id, time_id, attack_id, defense_id, entity_id)
    g.geo_id,
    t.time_id,
    
    COALESCE(
        a_specific.attack_id, 
        a_category.attack_id, 
        (SELECT attack_id FROM attack_dimension WHERE attack_type = 'Unknown' LIMIT 1)
    ) as attack_id,

    COALESCE(
        d.defense_id, 
        (SELECT defense_id FROM defense_dimension WHERE defense_mechanism = 'Unknown' LIMIT 1)
    ) as defense_id,

    COALESCE(
        e.entity_id, 
        (SELECT entity_id FROM entity_dimension WHERE entity_name = 'Unknown' LIMIT 1)
    ) as entity_id,

    s.affected_users,
    s.resolution_time_hours,
    b.records as records_lost

FROM staging_global_threats s

FULL OUTER JOIN staging_breaches b 
    ON s.country = b.country 
    AND s.year = b.year 
    AND s.unified_attack_category = b.unified_attack_category 
    AND s.unified_industry = b.unified_industry

JOIN geography_dimension g ON g.country = COALESCE(s.country, b.country)
JOIN time_dimension t      ON t.year    = COALESCE(s.year, b.year)

LEFT JOIN (
    SELECT DISTINCT ON (attack_type) attack_id, attack_type 
    FROM attack_dimension
) a_specific ON s.attack_type = a_specific.attack_type

LEFT JOIN (
    SELECT DISTINCT ON (unified_category) attack_id, unified_category 
    FROM attack_dimension
) a_category ON b.unified_attack_category = a_category.unified_category

LEFT JOIN (
    SELECT DISTINCT ON (defense_mechanism) defense_id, defense_mechanism 
    FROM defense_dimension
) d ON s.defense_mechanism = d.defense_mechanism

LEFT JOIN entity_dimension e ON b.entity = e.entity_name

ON CONFLICT (geo_id, time_id, attack_id, defense_id, entity_id) 
DO UPDATE SET
    records_lost = COALESCE(EXCLUDED.records_lost, fact_cyber_incidents.records_lost),
    affected_users = COALESCE(EXCLUDED.affected_users, fact_cyber_incidents.affected_users),
    resolution_time_hours = COALESCE(EXCLUDED.resolution_time_hours, fact_cyber_incidents.resolution_time_hours);



DO $$
BEGIN
    RAISE NOTICE 'Fact table insert completed at % ✓', NOW();
    RAISE NOTICE 'Total rows in cyber_security_attack: % ✓', (SELECT COUNT(*) FROM fact_cyber_incidents);
END $$;


-- Insert Fact Net Crime Stats
INSERT INTO fact_net_crime_stats (geo_id, time_id, total_complaints, total_financial_losses)
SELECT 
    g.geo_id,
    t.time_id,
    n.complaints,
    n.losses
FROM staging_net_crime n
JOIN geography_dimension g ON n.country = g.country
JOIN time_dimension t ON n.year = t.year;

DO $$
BEGIN
    RAISE NOTICE 'Fact table insert completed at % ✓', NOW();
    RAISE NOTICE 'Total rows in cyber_security_attack: % ✓', (SELECT COUNT(*) FROM fact_net_crime_stats);
END $$;
