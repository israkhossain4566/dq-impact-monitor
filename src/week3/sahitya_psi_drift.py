import numpy as np 
from src.week1.jaimil_db_utilities import fetchall,execute 

 

NUM_COLS = ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"] 

 

def get_vals(table, col): 

    rows = fetchall(f"SELECT {col} AS v FROM {table} WHERE {col} IS NOT NULL;") 

    return np.array([float(r["v"]) for r in rows], dtype=float) 

 

def psi(expected, actual, bins=10, eps=1e-6): 

    q = np.quantile(expected, np.linspace(0, 1, bins + 1)) 

    q[0], q[-1] = -np.inf, np.inf 

    e_hist, _ = np.histogram(expected, bins=q) 

    a_hist, _ = np.histogram(actual, bins=q) 

    e = e_hist / max(e_hist.sum(), 1) 

    a = a_hist / max(a_hist.sum(), 1) 

    e = np.clip(e, eps, 1) 

    a = np.clip(a, eps, 1) 

    return float(np.sum((a - e) * np.log(a / e))) 

 

def run(): 

    for col in NUM_COLS: 

        tr = get_vals("training_data", col) 

        pr = get_vals("production_data", col) 

        if len(tr) < 50 or len(pr) < 50: 

            continue 

        score = psi(tr, pr, bins=10) 

        execute( 

            "INSERT INTO drift_log(method, column_name, drift_score, p_value, details) VALUES (%s,%s,%s,%s,%s);", 

            ("psi", col, score, None, "PSI using train quantile bins=10") 

        ) 

    print("PSI drift logged.") 

 

if __name__ == "__main__": 

    run() 

