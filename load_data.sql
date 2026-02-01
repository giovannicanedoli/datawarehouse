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
    unified_industry TEXT,
    continent TEXT,     
    nation_welfare TEXT, 
    west_or_east TEXT,
    pandemic_era TEXT,
    is_leap_year BOOLEAN
);

CREATE TABLE IF NOT EXISTS staging_net_crime (
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

CREATE TABLE IF NOT EXISTS staging_breaches (
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

-- Create Fact Table
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

-- 5. Insert Dimensions
INSERT INTO geography_dimension (country, continent, nation_welfare, west_or_east) 
SELECT DISTINCT country, continent, nation_welfare, west_or_east 
FROM staging_global_threats
UNION 
SELECT DISTINCT country, continent, nation_welfare, west_or_east 
FROM staging_net_crime
UNION
SELECT DISTINCT country, continent, nation_welfare, west_or_east
FROM staging_breaches;

INSERT INTO time_dimension (year, pandemic_era, is_leap_year)
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_global_threats
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_breaches
UNION
SELECT DISTINCT year, pandemic_era, is_leap_year FROM staging_net_crime;

INSERT INTO attack_dimension (attack_type, attack_source, vulnerability_type, unified_category)
SELECT DISTINCT attack_type, attack_source, vulnerability_type, unified_attack_category
FROM staging_global_threats s;

INSERT INTO attack_dimension (attack_type, attack_source, unified_category) 
VALUES ('Unknown', 'Unknown', 'Unknown');


INSERT INTO defense_dimension (defense_mechanism, vulnerability_type)
SELECT DISTINCT defense_mechanism, vulnerability_type FROM staging_global_threats WHERE defense_mechanism IS NOT NULL;
INSERT INTO defense_dimension (defense_mechanism, vulnerability_type) 
VALUES ('Unknown', 'Unknown');

INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records)
SELECT DISTINCT ON (entity)
    entity,
    unified_industry, 
    organization_type,
    records
FROM staging_breaches s;
INSERT INTO entity_dimension (entity_name, industry, org_type, stolen_records) 
VALUES ('Unknown', 'Unknown', 'Unknown', 0);


INSERT INTO cyber_security_attack (
    geo_id, attack_id, defense_id, entity_id, time_id, 
    complaints, losses, affected_users, resolution_time_hours, records_lost
)
SELECT 
    geo_id, 
    attack_id, 
    defense_id, 
    entity_id, 
    time_id,
    SUM(complaints) as complaints,
    SUM(losses) as losses,
    SUM(affected_users) as affected_users,
    ROUND(AVG(resolution_time_hours))::int as resolution_time_hours,
    SUM(records_lost) as records_lost
FROM (

    SELECT 
        g.geo_id, 
        distinct_attacks.attack_id,
        distinct_defenses.defense_id, 
        (SELECT entity_id FROM entity_dimension WHERE entity_name = 'Unknown' LIMIT 1) as entity_id,
        t.time_id,
        NULL::bigint as complaints,
        NULL::bigint as losses,
        s.affected_users::bigint as affected_users,
        s.resolution_time_hours::int as resolution_time_hours,
        NULL::bigint as records_lost
    FROM staging_global_threats s
    JOIN geography_dimension g ON s.country = g.country 
    JOIN time_dimension t      ON s.year = t.year
    --JOIN attack_dimension a    ON s.attack_type = a.attack_type
    --JOIN defense_dimension d   ON s.defense_mechanism = d.defense_mechanism
    JOIN (SELECT DISTINCT ON (a.attack_type) a.attack_id, a.attack_type FROM attack_dimension a)
     distinct_attacks ON s.attack_type = distinct_attacks.attack_type
    JOIN (SELECT DISTINCT ON (d.defense_mechanism) d.defense_id, d.defense_mechanism FROM defense_dimension d) 
    distinct_defenses ON s.defense_mechanism = distinct_defenses.defense_mechanism


    UNION ALL

    -- Data from Net Crime
    SELECT 
        g.geo_id,
        (SELECT attack_id FROM attack_dimension WHERE attack_type = 'Unknown' LIMIT 1) as attack_id,
        (SELECT defense_id FROM defense_dimension WHERE defense_mechanism = 'Unknown' LIMIT 1) as defense_id,
        (SELECT entity_id FROM entity_dimension WHERE entity_name = 'Unknown' LIMIT 1) as entity_id,
        t.time_id,
        n.complaints,
        n.losses,
        NULL::bigint,
        NULL::int,
        NULL::bigint
    FROM staging_net_crime n
    JOIN geography_dimension g ON n.country = g.country 
    JOIN time_dimension t      ON n.year = t.year

    UNION ALL

    -- Data from Breaches
    SELECT 
        g.geo_id,
        COALESCE(distinct_attacks.attack_id, (SELECT attack_id FROM attack_dimension WHERE attack_type = 'Unknown' LIMIT 1)) as attack_id,
        (SELECT defense_id FROM defense_dimension WHERE defense_mechanism = 'Unknown' LIMIT 1) as defense_id,
        e.entity_id,
        t.time_id,
        NULL::bigint,
        NULL::bigint,
        NULL::bigint,
        NULL::int,
        b.records
    FROM staging_breaches b
    JOIN geography_dimension g ON b.country = g.country 
    JOIN time_dimension t      ON b.year = t.year
    JOIN entity_dimension e    ON b.entity = e.entity_name
    --LEFT JOIN attack_dimension a ON b.unified_attack_category = a.unified_category
    LEFT JOIN (SELECT distinct on (a.attack_type) a.attack_id, a.attack_type, a.unified_category
     FROM attack_dimension a) distinct_attacks ON b.unified_attack_category = distinct_attacks.unified_category

) as combined_data

GROUP BY geo_id, attack_id, defense_id, entity_id, time_id;



DO $$
BEGIN
    RAISE NOTICE 'Fact table insert completed at % ✓', NOW();
    RAISE NOTICE 'Total rows in cyber_security_attack: % ✓', (SELECT COUNT(*) FROM cyber_security_attack);
END $$;