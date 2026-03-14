from src.week1.jaimil_db_utilities import fetchall, execute

NUM_COLS = ["age","fnlwgt","education_num","capital_gain","capital_loss","hours_per_week"]

def stats(table, col):
    r = fetchall(f"SELECT AVG({col}) AS mean, STDDEV_SAMP({col}) AS sd FROM {table} WHERE {col} IS NOT NULL;")[0]
    return float(r["mean"]), float(r["sd"]) if r["sd"] else 0.0

def run():
    for col in NUM_COLS:
        tr_m, tr_s = stats("training_data", col)
        pr_m, pr_s = stats("production_data", col)
        score = abs(tr_m - pr_m)
        execute(
            "INSERT INTO drift_log(method, column_name, drift_score, p_value, details) VALUES (%s,%s,%s,%s,%s);",
            ("mean_shift", col, float(score), None,
             f"train_mean={tr_m},prod_mean={pr_m},train_sd={tr_s},prod_sd={pr_s}")
        )
    print("mean/std drift logged.")

if __name__ == "__main__":
    run()
