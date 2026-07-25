# Data Quality Impact Monitor

Data Quality Impact Monitor is a Python and SQL project for profiling datasets, detecting data quality issues, monitoring drift, and evaluating how corrupted or shifted data affects machine learning model performance.

The project combines data profiling, anomaly detection, statistical drift checks, and model impact analysis to show how data quality problems can affect downstream predictive systems.

## Features

- Missing-value profiling
- Numeric and categorical data profiling
- Schema and constraint checks
- Range-based validation
- Z-score anomaly detection
- Data corruption simulation
- Drift detection using statistical methods
- PSI, KS-test, mean, and standard deviation drift analysis
- Model performance comparison on clean and corrupted data
- Feature impact and ablation analysis
- Final impact ranking and report generation

## Tech Stack

- Python
- Pandas
- NumPy
- SciPy
- Scikit-learn
- Matplotlib
- PostgreSQL
- psycopg2
- Docker Compose

## Project Structure

```text
dq-impact-monitor/
|-- data/                 # Input datasets and generated data files
|-- reports/              # Output reports, figures, and analysis results
|-- sql/                  # SQL scripts for profiling, constraints, and drift tables
|-- src/
|   |-- week1/             # Dataset preparation and basic profiling
|   |-- week2/             # Corruption injection, range checks, and anomaly detection
|   |-- week3/             # Drift detection, model evaluation, and impact analysis
|   |-- week4/             # Extended analysis modules
|   |-- week5/             # Final project components
|   |-- upto_week2.py
|   `-- upto_week3.py
|-- docker-compose.yml     # PostgreSQL setup
|-- requirements.txt
`-- README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/israkhossain4566/dq-impact-monitor.git
cd dq-impact-monitor
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

If you want to use the PostgreSQL workflow, start the database with Docker Compose:

```bash
docker-compose up -d
```

The SQL scripts are stored in the `sql/` folder and include profiling tables, schema constraints, and drift-related tables.

## Running the Project

Run the Week 1 profiling workflow:

```bash
python -m src.week1.run_all
```

Run the Week 2 anomaly and validation workflow:

```bash
python -m src.week2.run_all_week2
```

Run the Week 3 drift and model impact workflow:

```bash
python -m src.week3.run_all_week3
```

## SQL Scripts

The `sql/` folder contains:

- `missing_profile.sql` - missing-value profiling
- `numeric_profile.sql` - numeric feature profiling
- `categorical_profile.sql` - categorical feature profiling
- `week1_Israk_schema.sql` - initial schema setup
- `week2_israk_constraints_tables.sql` - validation and constraint tables
- `week3_israk_drift_table.sql` - drift monitoring tables

## Analysis Workflow

1. Prepare and load the dataset
2. Profile missing, numeric, and categorical values
3. Define schema rules and validation constraints
4. Inject controlled data corruptions
5. Detect anomalies and range violations
6. Measure data drift across dataset versions
7. Train and evaluate machine learning models
8. Compare clean vs corrupted performance
9. Rank features and issues by downstream impact

## Purpose

This project demonstrates how data quality issues can be detected, measured, and connected to machine learning model performance. It is useful for understanding practical data monitoring workflows in applied machine learning and data engineering systems.

## Repository

[GitHub Repository](https://github.com/israkhossain4566/dq-impact-monitor)
