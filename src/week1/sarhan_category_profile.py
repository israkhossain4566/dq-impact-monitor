from src.week1.jaimil_db_utilities import fetchall, execute 

 

CAT_COLS = ["workclass","education","marital_status","occupation","relationship","race","sex","native_country","income"] 

 

def top_value(table, col): 

    rows = fetchall( 

        f""" 

        SELECT {col} AS v, COUNT(*) AS c 

        FROM {table} 

        GROUP BY {col} 

        ORDER BY c DESC NULLS LAST 

        LIMIT 1; 

        """ 

    ) 

    if not rows: 

        return None, 0 

    return rows[0]["v"], rows[0]["c"] 

 

def run(ds, table): 

    for col in CAT_COLS: 

        d = fetchall(f"SELECT COUNT(DISTINCT {col}) AS dc FROM {table};")[0]["dc"] 

        tv, tc = top_value(table, col) 

        execute( 

            """ 

            INSERT INTO category_profile(dataset_name, column_name, distinct_count, top_value, top_count) 

            VALUES (%s,%s,%s,%s,%s) 

            ON CONFLICT (dataset_name, column_name) DO UPDATE SET 

              distinct_count=EXCLUDED.distinct_count, 

              top_value=EXCLUDED.top_value, 

              top_count=EXCLUDED.top_count; 

            """, 

            (ds, col, int(d), tv, int(tc)) 

        ) 

 

if __name__ == "__main__": 

    run("train", "training_data") 

    run("prod", "production_data") 

    print(" category profiles saved.") 
