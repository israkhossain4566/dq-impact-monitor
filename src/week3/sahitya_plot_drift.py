import os 

import numpy as np 

import matplotlib.pyplot as plt 

from src.week1.jaimil_db_utilities import fetchall 

 

OUT_DIR = "reports/figures" 

NUM_COLS = ["age","education_num","hours_per_week","capital_gain"] 

 

def vals(table, col): 

    rows = fetchall(f"SELECT {col} AS v FROM {table} WHERE {col} IS NOT NULL;") 

    return np.array([float(r["v"]) for r in rows], dtype=float) 

 

def run(): 

    os.makedirs(OUT_DIR, exist_ok=True) 

    for col in NUM_COLS: 

        tr = vals("training_data", col) 

        pr = vals("production_data", col) 

        plt.figure() 

        plt.hist(tr, bins=30, alpha=0.5, label="train") 

        plt.hist(pr, bins=30, alpha=0.5, label="prod") 

        plt.title(f"Distribution: {col}") 

        plt.legend() 

        path = os.path.join(OUT_DIR, f"drift_{col}.png") 

        plt.savefig(path, dpi=200, bbox_inches="tight") 

        plt.close() 

    print("drift plots saved in reports/figures/") 

 

if __name__ == "__main__": 

    run() 