import os
import sys
import subprocess
from pathlib import Path

ROOT    = Path(__file__).resolve().parent
SQL_DIR = ROOT.parent.parent / "sql"
SRC_DIR = ROOT

def run_command(cmd, env=None):
    print("\n" + "=" * 80)
    print("RUNNING:", " ".join(str(c) for c in cmd))
    print("=" * 80)
    subprocess.run(cmd, check=True, env=env)

def main():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT.parent.parent) + os.pathsep + env.get("PYTHONPATH", "")

    required = ["DB_NAME", "DB_USER", "DB_PASS"]
    missing = [x for x in required if not env.get(x)]
    if missing:
        print("Warning: these env variables are not set:", ", ".join(missing))
        print("Scripts will fall back to their own defaults.")

    run_command([
        "psql",
        "-h", env.get("DB_HOST", "localhost"),
        "-p", env.get("DB_PORT", "5432"),
        "-U", env.get("DB_USER", "dq"),
        "-d", env.get("DB_NAME", "dqdb"),
        "-f", str(SQL_DIR / "week3_israk_drift_table.sql"),
    ], env=env)

    run_command([
        "psql",
        "-h", env.get("DB_HOST", "localhost"),
        "-p", env.get("DB_PORT", "5432"),
        "-U", env.get("DB_USER", "dq"),
        "-d", env.get("DB_NAME", "dqdb"),
        "-c", "TRUNCATE TABLE drift_log;",
    ], env=env)

    scripts = [
        "israk_mean_std_drift.py",
        "israk_ks_drift.py",
        "sahitya_drift_report.py",
        "jaimil_features.py",
        "jaimil_train_logreg.py",
        "jaimil_train_rf.py",
        "sahitya_psi_drift.py",
        "sahitya_plot_drift.py",
        "dev_eval_prod_clean.py",
        "dev_eval_after_corruption.py",
        "dev_feature_impact.py",
        "final_impact_ranking.py",
        "sarhan_anomaly_eval.py",
        "sarhan_drift_eval.py",
        "israk_ablation.py",
        "israk_final_figures.py",
    ]
    for script in scripts:
        run_command([sys.executable, str(SRC_DIR / script)], env=env)

    print("\nAll Week 3 scripts ran successfully.")

if __name__ == "__main__":
    main()
