DROP TABLE IF EXISTS numeric_profile CASCADE;

CREATE TABLE numeric_profile (
    id SERIAL PRIMARY KEY,
    dataset TEXT NOT NULL,
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    n BIGINT NOT NULL,
    n_null BIGINT NOT NULL,
    min DOUBLE PRECISION,
    max DOUBLE PRECISION,
    mean DOUBLE PRECISION,
    std DOUBLE PRECISION,
    median DOUBLE PRECISION,
    p25 DOUBLE PRECISION,
    p75 DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(dataset, table_name, column_name)
);

CREATE INDEX IF NOT EXISTS idx_numeric_profile
ON numeric_profile(dataset, table_name, column_name);
