"""
ga_demo.py — DQ Project Demo (Weeks 1 & 2)
Run this to walk through everything the team built, live in the terminal.

Usage:
    python ga_demo.py

Requirements:
    pip install psycopg2-binary tabulate colorama
    DB must be running and populated (run run_all.py + run_all_week2.py first)

Env vars (optional, these are the defaults):
    DB_HOST=localhost  DB_PORT=5432  DB_NAME=dqdb  DB_USER=dq  DB_PASS=dqpass
"""

import os
import sys
import time
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    from tabulate import tabulate
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Missing packages. Run:  pip install psycopg2-binary tabulate colorama")
    sys.exit(1)

# ── colours ──────────────────────────────────────────────────────────────────
C  = Fore.CYAN
G  = Fore.GREEN
Y  = Fore.YELLOW
R  = Fore.RED
M  = Fore.MAGENTA
W  = Fore.WHITE
DIM = Style.DIM
B  = Style.BRIGHT
RST = Style.RESET_ALL

# ── db connection ─────────────────────────────────────────────────────────────
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "dqdb"),
        user=os.getenv("DB_USER", "dq"),
        password=os.getenv("DB_PASS", "dqpass"),
    )

def query(sql, params=None):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

# ── helpers ───────────────────────────────────────────────────────────────────
def banner(title):
    width = 72
    print()
    print(C + "═" * width)
    print(C + B + f"  {title}")
    print(C + "═" * width + RST)

def section(title, author=""):
    print()
    tag = f"  [{author}]" if author else ""
    print(Y + B + f"▶ {title}" + DIM + tag + RST)
    print(Y + "─" * 60 + RST)

def ok(msg):
    print(G + "  ✓ " + W + msg + RST)

def info(msg):
    print(DIM + "    " + msg + RST)

def show_table(rows, headers="keys", max_rows=10):
    if not rows:
        print(DIM + "    (no rows)" + RST)
        return
    data = [dict(r) for r in rows[:max_rows]]
    print(tabulate(data, headers=headers, tablefmt="rounded_outline"))
    if len(rows) > max_rows:
        print(DIM + f"    … {len(rows) - max_rows} more rows not shown" + RST)

def pause(msg="Press ENTER to continue..."):
    print()
    input(DIM + f"  ── {msg} " + RST)

# ─────────────────────────────────────────────────────────────────────────────
#  DEMO SECTIONS
# ─────────────────────────────────────────────────────────────────────────────

def intro():
    banner("DQ PROJECT DEMO  —  Weeks 1 & 2")
    print(f"""
{W}This demo walks through everything the team built:

  {C}WEEK 1{RST}  Schema design · Data loading · Profiling (numeric, categorical, missing)
  {C}WEEK 2{RST}  Anomaly detection (range + z-score) · Corruption injection · Summary report

{DIM}Team: Md Israk Hossain · Sahitya · Jaimil · Dev · Sarhan · Pavan{RST}
""")
    pause("Ready? Press ENTER to start...")


def demo_week1_tables():
    banner("WEEK 1 — DATABASE TABLES  [Md Israk Hossain]")
    info("Israk designed all 5 tables. Let's confirm they exist and check their row counts.")

    section("Core data tables", "Israk · week1_Israk_schema.sql")
    rows = query("""
        SELECT
            'training_data'  AS table_name, COUNT(*) AS rows FROM training_data
        UNION ALL
        SELECT
            'production_data', COUNT(*) FROM production_data
    """)
    show_table(rows)
    ok("training_data and production_data exist and are populated")

    section("Profile tables", "Israk · missing_profile.sql · numeric_profile.sql · categorical_profile.sql")
    rows = query("""
        SELECT table_name, pg_relation_size(quote_ident(table_name))::bigint AS size_bytes
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name IN ('missing_profile','numeric_profile','categorical_profile')
        ORDER BY table_name
    """)
    show_table(rows)
    ok("All 3 profile tables exist")
    pause()


def demo_week1_load():
    banner("WEEK 1 — DATA LOADING  [Sahitya · Md Israk Hossain]")

    section("Sample rows — training_data", "Israk · prepare_dataset.py  +  Sahitya · sahitya_load_csv.py")
    info("Israk prepared the CSVs from raw UCI files. Sahitya bulk-loaded them via COPY.")
    rows = query("SELECT age, workclass, education, occupation, sex, income FROM training_data LIMIT 6")
    show_table(rows)

    section("Sample rows — production_data")
    rows = query("SELECT age, workclass, education, occupation, sex, income FROM production_data LIMIT 6")
    show_table(rows)
    ok("Both tables loaded successfully from adult_train.csv and adult_prod.csv")
    pause()


def demo_week1_numeric():
    banner("WEEK 1 — NUMERIC PROFILING  [Dev · dev_numeric_profile.py]")
    info("Dev computed min/max/mean/std/median/quartiles for all numeric columns.")
    info("These stats become the reference for Week 2 z-score anomaly detection.")

    rows = query("""
        SELECT dataset, column_name, n, n_null,
               ROUND(mean::numeric,2)   AS mean,
               ROUND(std::numeric,2)    AS std,
               ROUND(min::numeric,2)    AS min,
               ROUND(max::numeric,2)    AS max,
               ROUND(median::numeric,2) AS median
        FROM numeric_profile
        WHERE dataset = 'train'
        ORDER BY column_name
    """)
    show_table(rows)
    ok("numeric_profile populated for training_data")
    pause()


def demo_week1_missing():
    banner("WEEK 1 — MISSING VALUE PROFILING  [Pavan · missing_profile.py]")
    info("Pavan tracked null counts and null % for every column in both datasets.")

    rows = query("""
        SELECT dataset, column_name, n, n_null,
               ROUND(null_pct::numeric * 100, 2) AS null_pct_pct
        FROM missing_profile
        ORDER BY dataset, null_pct DESC
        LIMIT 20
    """)
    show_table(rows)
    ok("missing_profile populated — top columns by null % shown above")
    pause()


def demo_week1_categorical():
    banner("WEEK 1 — CATEGORICAL PROFILING  [Sarhan · sarhan_category_profile.py]")
    info("Sarhan counted frequency and % share of every value in all text columns.")
    info("Showing 'workclass' distribution in training data as an example:")

    rows = query("""
        SELECT category, frequency,
               ROUND(pct::numeric * 100, 1) AS pct_of_total
        FROM categorical_profile
        WHERE dataset = 'train' AND column_name = 'workclass'
        ORDER BY frequency DESC
    """)
    show_table(rows)

    info("And 'income' distribution (the target column):")
    rows = query("""
        SELECT category, frequency,
               ROUND(pct::numeric * 100, 1) AS pct_of_total
        FROM categorical_profile
        WHERE dataset = 'train' AND column_name = 'income'
        ORDER BY frequency DESC
    """)
    show_table(rows)
    ok("categorical_profile populated for all 9 text columns")
    pause()


def demo_week2_constraints():
    banner("WEEK 2 — MIN/MAX CONSTRAINTS  [Sahitya · sahitya_infer_minmax.py]")
    info("Sahitya inferred valid min/max boundaries from training data.")
    info("These rules are stored in the constraints table and used by the range checker.")

    rows = query("""
        SELECT column_name, rule_type, rule_value
        FROM constraints
        ORDER BY column_name, rule_type
    """)
    show_table(rows)
    ok("constraints table populated — 2 rules per numeric column (min + max)")
    pause()


def demo_week2_corruption():
    banner("WEEK 2 — CORRUPTION INJECTION  [Sarhan · sarhan_inject_corruption.py]")
    info("Sarhan deliberately planted bad values in production_data to test the detectors.")
    info("Let's verify the bad data is actually in the table:")

    section("Rows with negative age (should be 5)")
    rows = query("SELECT id, age, hours_per_week, capital_gain FROM production_data WHERE age < 0")
    show_table(rows)

    section("Rows with hours_per_week > 168 (impossible)")
    rows = query("SELECT id, age, hours_per_week FROM production_data WHERE hours_per_week > 168")
    show_table(rows)

    section("Rows with extreme capital_gain (= 999999)")
    rows = query("SELECT id, capital_gain FROM production_data WHERE capital_gain = 999999")
    show_table(rows)

    ok("Corruption confirmed in production_data")
    pause()


def demo_week2_range():
    banner("WEEK 2 — RANGE ANOMALY DETECTION  [Jaimil · jaimil_range_check.py]")
    info("Jaimil's script scanned every production row against the min/max constraints.")
    info("Any value outside the trained range gets logged to anomaly_log.")

    rows = query("""
        SELECT column_name, row_id, value, reason
        FROM anomaly_log
        WHERE detector = 'range'
        ORDER BY column_name, row_id
    """)
    show_table(rows)
    count = query("SELECT COUNT(*) AS n FROM anomaly_log WHERE detector = 'range'")[0]["n"]
    ok(f"Range detector found {count} anomalies → logged to anomaly_log")
    pause()


def demo_week2_zscore():
    banner("WEEK 2 — Z-SCORE ANOMALY DETECTION  [Dev · dev_zscore_anomaly.py]")
    info("Dev's script flagged production values more than 3 standard deviations")
    info("from the training mean — catching subtle statistical outliers.")

    rows = query("""
        SELECT column_name, row_id, value,
               ROUND(score::numeric, 2) AS z_score, reason
        FROM anomaly_log
        WHERE detector = 'zscore'
        ORDER BY ABS(score) DESC
    """)
    show_table(rows)
    count = query("SELECT COUNT(*) AS n FROM anomaly_log WHERE detector = 'zscore'")[0]["n"]
    ok(f"Z-score detector found {count} anomalies → logged to anomaly_log")
    pause()


def demo_week2_summary():
    banner("WEEK 2 — ANOMALY SUMMARY  [Md Israk Hossain · israk_anomaly_summary.py]")
    info("Israk's summary script gives a quick overview of all anomalies found,")
    info("grouped by which detector caught them and which column they're in.")

    print()
    print(M + B + "  === Anomaly Summary ===" + RST)
    rows = query("""
        SELECT detector, column_name, COUNT(*) AS anomaly_count
        FROM anomaly_log
        GROUP BY detector, column_name
        ORDER BY anomaly_count DESC, detector, column_name
    """)
    if not rows:
        print(DIM + "  No anomalies found." + RST)
    else:
        for row in rows:
            det   = row["detector"]
            col   = row["column_name"]
            cnt   = row["anomaly_count"]
            color = R if det == "range" else M
            print(f"  {color}{det:>7}{RST}  {W}{col:<20}{RST}  {Y}{cnt} anomalies{RST}")

    print()
    total = query("SELECT COUNT(*) AS n FROM anomaly_log")[0]["n"]
    ok(f"Total anomalies logged: {total}")
    pause()


def finale():
    banner("DEMO COMPLETE")
    print(f"""
{G}{B}  Everything working end-to-end! Here's the full pipeline summary:
{RST}
  {C}WEEK 1{RST}
  {DIM}Israk{RST}    → Designed all 5 database tables (schema SQL files)
  {DIM}Israk{RST}    → Prepared raw CSVs from UCI dataset  (prepare_dataset.py)
  {DIM}Sahitya{RST}  → Bulk-loaded CSVs into Postgres      (sahitya_load_csv.py)
  {DIM}Jaimil{RST}   → Shared DB utilities used by all     (jaimil_db_utilities.py)
  {DIM}Dev{RST}      → Numeric statistics profiling        (dev_numeric_profile.py)
  {DIM}Pavan{RST}    → Missing value profiling             (missing_profile.py)
  {DIM}Sarhan{RST}   → Categorical frequency profiling     (sarhan_category_profile.py)
  {DIM}Israk{RST}    → Master runner                       (run_all.py)

  {C}WEEK 2{RST}
  {DIM}Israk{RST}    → Designed constraints + anomaly_log  (week2_israk_constraints_tables.sql)
  {DIM}Sahitya{RST}  → Learned min/max rules from training (sahitya_infer_minmax.py)
  {DIM}Sarhan{RST}   → Injected test corruption            (sarhan_inject_corruption.py)
  {DIM}Jaimil{RST}   → Range-based anomaly detection       (jaimil_range_check.py)
  {DIM}Dev{RST}      → Z-score anomaly detection           (dev_zscore_anomaly.py)
  {DIM}Israk{RST}    → Anomaly summary report              (israk_anomaly_summary.py)
  {DIM}Israk{RST}    → Master runner                       (run_all_week2.py)
""")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    try:
        conn = get_conn()
        conn.close()
    except Exception as e:
        print(R + f"\n  ✗ Cannot connect to database: {e}")
        print(DIM + "  Make sure Postgres is running and run_all.py + run_all_week2.py have been executed first.\n")
        sys.exit(1)

    intro()
    demo_week1_tables()
    demo_week1_load()
    demo_week1_numeric()
    demo_week1_missing()
    demo_week1_categorical()
    demo_week2_constraints()
    demo_week2_corruption()
    demo_week2_range()
    demo_week2_zscore()
    demo_week2_summary()
    finale()


if __name__ == "__main__":
    main()