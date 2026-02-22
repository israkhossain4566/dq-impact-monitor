DROP TABLE IF EXISTS training_data;
DROP TABLE IF EXISTS production_data;

CREATE TABLE training_data (
  id SERIAL PRIMARY KEY,
  age INT,
  workclass TEXT,
  fnlwgt INT,
  education TEXT,
  education_num INT,
  marital_status TEXT,
  occupation TEXT,
  relationship TEXT,
  race TEXT,
  sex TEXT,
  capital_gain INT,
  capital_loss INT,
  hours_per_week INT,
  native_country TEXT,
  income TEXT
);

CREATE TABLE production_data (LIKE training_data INCLUDING ALL);

CREATE TABLE column_profile (
  dataset_name TEXT NOT NULL,
  column_name TEXT NOT NULL,
  n BIGINT,
  n_null BIGINT,
  mean DOUBLE PRECISION,
  std DOUBLE PRECISION,
  min DOUBLE PRECISION,
  p25 DOUBLE PRECISION,
  median DOUBLE PRECISION,
  p75 DOUBLE PRECISION,
  max DOUBLE PRECISION,
  UNIQUE(dataset_name, column_name)
);