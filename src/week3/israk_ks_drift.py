import numpy as np
from scipy.stats import ks_2samp
from src.week1.jaimil_db_utilities import fetchall, execute

NUM_COLS = ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"]

def arr(table, col):
    rows = fetchall(f"SELECT {col} AS v FROM {table} WHERE {col} IS NOT NULL;")
    return np.array([float(r["v"]) for r in rows], dtype=float)

def run():
    for col in NUM_COLS:
        tr = arr("training_data", col)
        pr = arr("production_data", col)
        if len(tr) < 50 or len(pr) < 50:
            continue
        res = ks_2samp(tr, pr)
        execute(
            "INSERT INTO drift_log(method, column_name, drift_score, p_value, details) VALUES (%s,%s,%s,%s,%s);",
            ("ks", col, float(res.statistic), float(res.pvalue), "KS statistic + p-value")
        )
    print("KS drift logged.")

if __name__ == "__main__":
    run()
