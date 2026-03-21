from src.week1.jaimil_db_utilities import fetchall

def run():
    # Get PSI scores from drift log
    psi = fetchall(
        "SELECT column_name, drift_score "
        "FROM drift_log WHERE method='psi';"
    )
    psi_map = {r["column_name"]: float(r["drift_score"])
               for r in psi}

    # Feature importances from permutation results
    # (manually entered from dev_feature_impact.py output)
    importance = {
        "capital_gain":    0.21,
        "age":             0.19,
        "education_num":   0.16,
        "hours_per_week":  0.14,
        "capital_loss":    0.08,
        "fnlwgt":          0.06,
    }

    # Compute impact score = PSI x importance
    results = []
    for col, imp in importance.items():
        psi_score = psi_map.get(col, 0.0)
        impact = psi_score * imp
        results.append((col, psi_score, imp, impact))

    results.sort(key=lambda x: x[3], reverse=True)

    print(f"{'Feature':<20} {'PSI':>6} "
          f"{'Imp':>6} {'Impact':>8}")
    print("-" * 44)
    for col, psi_s, imp, impact in results:
        print(f"{col:<20} {psi_s:>6.3f} "
              f"{imp:>6.3f} {impact:>8.4f}")

if __name__ == "__main__":
    run()
