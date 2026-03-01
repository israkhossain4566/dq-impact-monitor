import psycopg2

DB = {
    "host": "localhost",
    "database": "dqdb",
    "user": "dq",
    "password": "dqpass",
}

def fetch_one(cur, q: str) -> int:
    cur.execute(q)
    return cur.fetchone()[0]

def main() -> None:
    conn = psycopg2.connect(**DB)
    cur = conn.cursor()

    train_rows = fetch_one(cur, "SELECT COUNT(*) FROM training_data;")
    prod_rows = fetch_one(cur, "SELECT COUNT(*) FROM production_data;")

    print(f"Training rows:   {train_rows}")
    print(f"Production rows: {prod_rows}")

    diff = abs(train_rows - prod_rows)
    pct = (diff / max(train_rows, 1)) * 100.0
    print(f"Row count diff:  {diff} ({pct:.2f}%)")

    if pct > 5:
        print("WARNING: Possible drift (production row count differs > 5% from training).")
    else:
        print("OK: Row count looks stable (<= 5% difference).")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()