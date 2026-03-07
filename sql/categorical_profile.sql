DROP TABLE IF EXISTS categorical_profile CASCADE;

CREATE TABLE categorical_profile (
    id SERIAL PRIMARY KEY,
    dataset TEXT NOT NULL,
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    category TEXT NOT NULL,
    frequency BIGINT NOT NULL,
    pct DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(dataset, table_name, column_name, category)
);

CREATE INDEX IF NOT EXISTS idx_categorical_profile
ON categorical_profile(dataset, table_name, column_name);
