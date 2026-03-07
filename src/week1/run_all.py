import os
import sys
import subprocess
from pathlib import Path


ROOT    = Path(__file__).resolve().parent      # src/week1
SQL_DIR = ROOT.parent.parent / "sql"           # ← ../../sql

# (the above SQL_DIR assignment already handles the correct path)
SRC_DIR = ROOT


def run_command(cmd, env=None):
    print("\n" + "=" * 80)
    print("RUNNING:", " ".join(cmd))
    print("=" * 80)
    subprocess.run(cmd, check=True, env=env)


def main():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC_DIR) + os.pathsep + env.get("PYTHONPATH", "")

    required = ["DB_NAME", "DB_USER", "DB_PASS"]
    missing = [x for x in required if not env.get(x)]
    if missing:
        print("Warning: these environment variables are not set:", ", ".join(missing))
        print("The scripts will still use their own default values if those are correct.")

    sql_files = [
        SQL_DIR / "week1_Israk_schema.sql",
        SQL_DIR / "numeric_profile.sql",
        SQL_DIR / "missing_profile.sql",
        SQL_DIR / "categorical_profile.sql",
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

    run_command([sys.executable, str(SRC_DIR / "prepare_dataset.py")], env=env)
    run_command([sys.executable, str(SRC_DIR / "sahitya_load_csv.py")], env=env)
    run_command([sys.executable, str(SRC_DIR / "dev_numeric_profile.py")], env=env)
    run_command([sys.executable, str(SRC_DIR / "missing_profile.py")], env=env)
    run_command([sys.executable, str(SRC_DIR / "sarhan_category_profile.py")], env=env)

    print("\nAll Week 1 scripts ran successfully.")


if __name__ == "__main__":
    main()
