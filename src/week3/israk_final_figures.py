import os
import matplotlib.pyplot as plt
from src.week1.jaimil_db_utilities import fetchall

OUT = "reports/figures"

def run():
    os.makedirs(OUT, exist_ok=True)
    rows = fetchall("""
        SELECT detector, COUNT(*) AS cnt
        FROM anomaly_log
        GROUP BY detector
        ORDER BY cnt DESC;
    """)
    det = [r["detector"] for r in rows]
    cnt = [int(r["cnt"]) for r in rows]
    plt.figure()
    plt.bar(det, cnt)
    plt.title("Anomalies by detector")
    plt.ylabel("count")
    path = os.path.join(OUT, "anomaly_by_detector.png")
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()
    print("saved", path)

if __name__ == "__main__":
    run()
