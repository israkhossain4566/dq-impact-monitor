from jaimil_db_utilities import execute 

 

CAT_COLS = ["workclass","education","marital_status","occupation","relationship","race","sex","native_country","income"] 

 
 

def run(ds, table):
    # compute frequency and percentage for every value in each categorical column
    for col in CAT_COLS:
        execute(
            ("""
            INSERT INTO categorical_profile(dataset, table_name, column_name, category, frequency, pct)
            SELECT
              %(ds)s,
              %(table)s,
              %(col)s,
              {col} AS category,
              COUNT(*) AS frequency,
              COUNT(*)::double precision / (SELECT COUNT(*) FROM {table}) AS pct
            FROM {table}
            GROUP BY {col}
            ON CONFLICT (dataset, table_name, column_name, category) DO UPDATE SET
              frequency=EXCLUDED.frequency,
              pct=EXCLUDED.pct;
            """
            ).format(col=col, table=table),
            {"ds": ds, "table": table, "col": col}
        )

 

if __name__ == "__main__": 

    run("train", "training_data") 

    run("prod", "production_data")

    print("category profiles saved.") 
