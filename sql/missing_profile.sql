DROP TABLE IF EXISTS missing_profile CASCADE;

CREATE TABLE missing_profile (
    id SERIAL PRIMARY KEY,
    dataset TEXT NOT NULL,
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    n BIGINT NOT NULL,
    n_null BIGINT NOT NULL,
    null_pct DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(dataset, table_name, column_name)
);

CREATE INDEX IF NOT EXISTS idx_missing_profile_ds_col
ON missing_profile(dataset, table_name, column_name);
