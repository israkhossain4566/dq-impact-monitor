CREATE TABLE IF NOT EXISTS constraints (
    column_name TEXT NOT NULL,
    rule_type TEXT NOT NULL,   -- min, max
    rule_value TEXT NOT NULL,
    UNIQUE(column_name, rule_type)
);

CREATE TABLE IF NOT EXISTS anomaly_log (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP DEFAULT NOW(),
    detector TEXT NOT NULL,    -- range, zscore
    column_name TEXT NOT NULL,
    row_id INT,
    value TEXT,
    score DOUBLE PRECISION,
    reason TEXT
);
CREATE INDEX IF NOT EXISTS idx_anomaly_log_detector_col
ON anomaly_log(detector, column_name);

CREATE INDEX IF NOT EXISTS idx_anomaly_log_row_id
ON anomaly_log(row_id);
