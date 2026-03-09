import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.week1.jaimil_db_utilities import fetchall, execute 

 

NUM_COLS = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"] 

 

def run(): 

  for col in NUM_COLS: 

    row = fetchall(f"SELECT MIN({col}) AS mn, MAX({col}) AS mx FROM training_data;")[0] 

    mn, mx = row["mn"], row["mx"] 
    execute("""INSERT INTO constraints(column_name, rule_type, rule_value) 
    VALUES (%s, 'min', %s) 

    ON CONFLICT (column_name, rule_type) DO UPDATE 
    SET rule_value = EXCLUDED.rule_value;  """,  (col, str(mn))) 

    

    execute("""INSERT INTO constraints(column_name, rule_type, rule_value) 
    VALUES (%s, 'max', %s) 

    ON CONFLICT (column_name, rule_type) DO UPDATE 

    SET rule_value = EXCLUDED.rule_value; """,(col, str(mx))) 

    

    print("Min/max constraints inferred from training_data.")

if __name__ == "__main__":
  run() 