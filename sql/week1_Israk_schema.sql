DROP TABLE IF EXISTS training_data CASCADE;
DROP TABLE IF EXISTS production_data CASCADE;

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
