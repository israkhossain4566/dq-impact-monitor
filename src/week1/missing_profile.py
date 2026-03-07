from jaimil_db_utilities import execute

ALL_COLS = [
    "age","workclass","fnlwgt","education","education_num","marital_status","occupation",
    "relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country","income"
]

SQL_TMPL = """
INSERT INTO missing_profile(dataset, table_name, column_name, n, n_null, null_pct)
SELECT
  %(ds)s,
  %(table)s,
  %(col)s,
  COUNT(*) AS n,
  SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS n_null,
  (SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END)::double precision / COUNT(*))
FROM {table}
ON CONFLICT (dataset, table_name, column_name) DO UPDATE SET
  n=EXCLUDED.n,
  n_null=EXCLUDED.n_null,
  null_pct=EXCLUDED.null_pct;
"""

def run(ds, table):
    for col in ALL_COLS:
        execute(SQL_TMPL.format(col=col, table=table), {"ds": ds, "col": col, "table": table})

if __name__ == "__main__":
    run("train", "training_data")
    run("prod", "production_data")
    print("missingness profiles saved.")
