from src.week1.jaimil_db_utilities import fetchall

def run():
    rows = fetchall(
        """
        SELECT detector, column_name, COUNT(*) AS cnt
        FROM anomaly_log
        GROUP BY detector, column_name
        ORDER BY cnt DESC, detector, column_name;
        """
    )

    print("=== Anomaly Summary ===")
    if not rows:
        print("No anomalies found.")
        return

    for row in rows:
        print(f"{row['detector']:>7}  {row['column_name']:<15}  {row['cnt']}")

if __name__ == "__main__":
    run()
