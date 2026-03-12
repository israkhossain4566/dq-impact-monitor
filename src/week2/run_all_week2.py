import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent      # src/week2
SQL_DIR = ROOT.parent.parent / "sql"        # ../../sql

SRC_DIR = ROOT

def run_command(cmd, env=None):
    print("\n" + "=" * 80)
    print("RUNNING:", " ".join(cmd))
    print("=" * 80)
    subprocess.run(cmd, check=True, env=env)

def main():
    env = os.environ.copy()
    src_root = ROOT.parent   # this is the 'src' directory containing week1, week2, etc.
    env["PYTHONPATH"] = str(src_root) + os.pathsep + env.get("PYTHONPATH", "")

    required = ["DB_NAME", "DB_USER", "DB_PASS"]
    missing = [x for x in required if not env.get(x)]
    if missing:
        print("Warning: these environment variables are not set:", ", ".join(missing))
        print("The scripts will still use their own default values if those are correct.")

    # SQL file for Week 2 tables (name matches the actual file in sql/)
    sql_files = [
        SQL_DIR / "week2_israk_constraints_tables.sql"
    ]

    for sql_file in sql_files:
        run_command([
            "psql",
            "-h", env.get("DB_HOST", "localhost"),
            "-p", env.get("DB_PORT", "5432"),
            "-U", env.get("DB_USER", "dq"),
            "-d", env.get("DB_NAME", "dqdb"),
            "-f", str(sql_file),
        ], env=env)

    # Optional cleanup so repeated runs don't duplicate anomalies
    run_command([
        "psql",
        "-h", env.get("DB_HOST", "localhost"),
        "-p", env.get("DB_PORT", "5432"),
        "-U", env.get("DB_USER", "dq"),
        "-d", env.get("DB_NAME", "dqdb"),
        "-c", "TRUNCATE TABLE anomaly_log;"
    ], env=env)

    # Run week2 scripts as modules to preserve package context for relative imports
    run_command([sys.executable, "-m", "week2.sahitya_infer_minmax"], env=env)
    run_command([sys.executable, "-m", "week2.jaimil_range_check"], env=env)
    run_command([sys.executable, "-m", "week2.dev_zscore_anomaly"], env=env)
    run_command([sys.executable, "-m", "week2.israk_anomaly_summary"], env=env)
    run_command([sys.executable, str(SRC_DIR / "week2.sarhan_lnject_corruptions_into_production.py")], env=env)

    print("\nAll Week 2 scripts ran successfully.")

if __name__ == "__main__":
    main()