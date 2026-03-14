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
        
    ]
    for script in scripts:
        run_command([sys.executable, str(SRC_DIR / script)], env=env)

    print("\nAll Week 3 scripts ran successfully.")

if __name__ == "__main__":
    main()