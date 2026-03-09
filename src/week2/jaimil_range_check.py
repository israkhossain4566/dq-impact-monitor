from src.week1.jaimil_db_utilities import fetchall, execute

NUM_COLS = ["age", "fnlwgt", "education_num", "capital_gain", "capital_loss", "hours_per_week"]

def get_rule(col, rule_type):
    rows = fetchall(
        "SELECT rule_value FROM constraints WHERE column_name = %s AND rule_type = %s;",
        (col, rule_type)
    )
    if not rows:
        raise ValueError(f"Missing constraint for column={col}, rule_type={rule_type}")
    return float(rows[0]["rule_value"])

def run():
    for col in NUM_COLS:
        mn = get_rule(col, "min")
        mx = get_rule(col, "max")

        rows = fetchall(f"SELECT id, {col} AS v FROM production_data WHERE {col} IS NOT NULL;")

        for row in rows:
            value = float(row["v"])
            if value < mn or value > mx:
                execute(
                    """
                    INSERT INTO anomaly_log(detector, column_name, row_id, value, score, reason)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    ("range", col, row["id"], str(value), None, f"out_of_range[{mn},{mx}]")
                )

    print("Range anomalies logged.")

if __name__ == "__main__":
    run()
