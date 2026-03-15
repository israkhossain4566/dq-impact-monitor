from src.week1.jaimil_db_utilities import fetchall

def run():
    ks = fetchall("SELECT column_name, drift_score, p_value FROM drift_log WHERE method='ks';")
    psi = fetchall("SELECT column_name, drift_score FROM drift_log WHERE method='psi';")

    psi_map = {r["column_name"]: float(r["drift_score"]) for r in psi}

    alerts = []
    for r in ks:
        col = r["column_name"]
        p = r["p_value"]
        psi_score = psi_map.get(col, 0.0)

        if (p is not None and float(p) < 0.01) or (psi_score > 0.2):
            alerts.append((col, float(r["drift_score"]), float(p) if p else None, psi_score))

    print("=== Drift Alerts ===")
    for col, ks_stat, p, psi_score in alerts:
        print(f"{col:<16} KS={ks_stat:.4f} p={p} PSI={psi_score:.4f}")

if __name__ == "__main__":
    run()