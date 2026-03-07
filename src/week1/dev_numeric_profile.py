from jaimil_db_utilities import execute 

 

NUM_COLS = ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"] 

 

SQL_TMPL = """

INSERT INTO numeric_profile(dataset, table_name, column_name, n, n_null, mean, std, min, p25, median, p75, max)

SELECT

  %(ds)s,

  %(table)s,

  %(col)s,

  COUNT({col}) AS n,

  SUM(CASE WHEN {col} IS NULL THEN 1 ELSE 0 END) AS n_null,

  AVG({col}::double precision),

  STDDEV_SAMP({col}::double precision),

  MIN({col}::double precision),

  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {col}),

  PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY {col}),

  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {col}),

  MAX({col}::double precision)

FROM {table}

ON CONFLICT (dataset, table_name, column_name) DO UPDATE SET

  n=EXCLUDED.n, n_null=EXCLUDED.n_null, mean=EXCLUDED.mean, std=EXCLUDED.std,

  min=EXCLUDED.min, p25=EXCLUDED.p25, median=EXCLUDED.median, p75=EXCLUDED.p75, max=EXCLUDED.max;

"""

 

def profile(ds, table): 

    for col in NUM_COLS: 

        execute(SQL_TMPL.format(col=col, table=table), {"ds": ds, "col": col, "table": table}) 

 

if __name__ == "__main__": 

    profile("train", "training_data") 

    profile("prod", "production_data")

    print("numeric profiles saved.") 
