import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.week1.jaimil_db_utilities import fetchall, execute 

NUM_COLS = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"] 

Z_THRESHOLD = 3.0 


def train_mean_std(col): 

    rows = fetchall( 
        """ 
        SELECT mean, std 
        FROM numeric_profile 
        WHERE dataset = %s 
        AND table_name = %s 
        AND column_name = %s; 
        """, 
        ("train", "training_data", col) 
    ) 

    if not rows: 
        raise ValueError(f"Training stats not found in numeric_profile for column: {col}") 

    mean_value = float(rows[0]["mean"]) if rows[0]["mean"] is not None else 0.0 
    std_value = float(rows[0]["std"]) if rows[0]["std"] is not None else 0.0 
    return mean_value, std_value 

def run(): 
    for col in NUM_COLS: 
        mu, sd = train_mean_std(col) 
        if sd == 0.0: 
            continue 
        rows = fetchall(f"SELECT id, {col} AS v FROM production_data WHERE {col} IS NOT NULL;") 
        for row in rows: 
            value = float(row["v"]) 
            z = (value - mu) / sd 
 
            if abs(z) > Z_THRESHOLD: 
                execute( 
                    """ 
                    INSERT INTO anomaly_log(detector, column_name, row_id, value, score, reason) 
                    VALUES (%s, %s, %s, %s, %s, %s); 
                    """, 
                    ("zscore", col, row["id"], str(value), float(z), f"|z|>{Z_THRESHOLD}") 
                ) 
    print("Z-score anomalies logged.") 
    
if __name__ == "__main__": 

    run() 