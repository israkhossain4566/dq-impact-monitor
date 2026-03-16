from src.week1.jaimil_db_utilities import fetchall

def count(detector=None):
    if detector is None:
        return fetchall("SELECT COUNT(*) AS c FROM anomaly_log;")[0]["c"]
    return fetchall("SELECT COUNT(*) AS c FROM anomaly_log WHERE detector=%s;", (detector,))[0]["c"]

def run():
    total = int(count())
    z = int(count("zscore"))
    r = int(count("range"))
    print("Total anomalies:", total)
    print("Range anomalies:", r)
    print("Z-score anomalies:", z)
    print("Ablation insight: if you remove range, remaining =", total - r)
    print("Ablation insight: if you remove zscore, remaining =", total - z)

if __name__ == "__main__":
    run()
