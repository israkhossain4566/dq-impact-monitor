CREATE TABLE IF NOT EXISTS drift_log (
    ts TIMESTAMP DEFAULT NOW(),
    method TEXT NOT NULL,
    column_name TEXT NOT NULL,
    drift_score DOUBLE PRECISION,
    p_value DOUBLE PRECISION,
    details TEXT
);
