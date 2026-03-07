import os 

import psycopg2 

 

TRAIN_PATH = os.getenv("TRAIN_CSV", "data/raw/adult_train.csv") 

PROD_PATH = os.getenv("PROD_CSV", "data/raw/adult_prod.csv") 

 

DB = dict( 

    host=os.getenv("DB_HOST", "localhost"), 

    port=int(os.getenv("DB_PORT", "5432")), 

    dbname=os.getenv("DB_NAME", "dqdb"), 

    user=os.getenv("DB_USER", "dq"), 

    password=os.getenv("DB_PASS", "dqpass"), 

) 

 

COLUMNS = ( 

    "age,workclass,fnlwgt,education,education_num,marital_status,occupation," 

    "relationship,race,sex,capital_gain,capital_loss,hours_per_week,native_country,income" 

) 

 

def copy_csv(conn, table, path): 

    if not os.path.exists(path): 

        raise FileNotFoundError(f"Missing CSV: {path}") 

    with conn.cursor() as cur, open(path, "r", encoding="utf-8") as f: 

        cur.copy_expert( 

            f"COPY {table}({COLUMNS}) FROM STDIN WITH (FORMAT csv, HEADER true)", 

            f 

        ) 

    conn.commit() 

 

def main(): 

    conn = psycopg2.connect(**DB) 

    print("Loading training CSV...") 

    copy_csv(conn, "training_data", TRAIN_PATH) 

    print("Loading production CSV...") 

    copy_csv(conn, "production_data", PROD_PATH) 

    conn.close() 

    print("Loaded both CSVs into Postgres.") 

 

if __name__ == "__main__": 

    main() 

 
