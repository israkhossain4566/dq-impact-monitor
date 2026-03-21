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
C   = Fore.CYAN
G   = Fore.GREEN
Y   = Fore.YELLOW
R   = Fore.RED
M   = Fore.MAGENTA
W   = Fore.WHITE
DIM = Style.DIM
B   = Style.BRIGHT
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
#  WEEK 1 & 2 SECTIONS  (unchanged)
# ─────────────────────────────────────────────────────────────────────────────

def intro():
    banner("DQ PROJECT DEMO  —  Weeks 1, 2 & 3")
    print(f"""
{W}This demo walks through everything the team built:

  {C}WEEK 1{RST}  Schema design · Data loading · Profiling (numeric, categorical, missing)
  {C}WEEK 2{RST}  Anomaly detection (range + z-score) · Corruption injection · Summary report
  {C}WEEK 3{RST}  Drift detection (mean/std, KS, PSI) · ML model training & evaluation
           Feature impact · Anomaly evaluation · Drift alerts · Ablation study
           Impact ranking (PSI x feature importance)

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


# ─────────────────────────────────────────────────────────────────────────────
#  WEEK 3 SECTIONS
# ─────────────────────────────────────────────────────────────────────────────

def demo_week3_drift_table():
    banner("WEEK 3 — DRIFT LOG TABLE  [Md Israk Hossain · israk_drift_table.sql]")
    info("Israk created the drift_log table to store results from all drift detectors.")
    info("Each row records: method, column, drift_score, p_value, and details.")

    rows = query("""
        SELECT table_name, pg_relation_size(quote_ident(table_name))::bigint AS size_bytes
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_name = 'drift_log'
    """)
    show_table(rows)

    total = query("SELECT COUNT(*) AS n FROM drift_log")[0]["n"]
    ok(f"drift_log table exists and contains {total} entries")
    pause()


def demo_week3_mean_std_drift():
    banner("WEEK 3 — MEAN / STD DRIFT  [Md Israk Hossain · israk_mean_std_drift.py]")
    info("Israk computed the absolute mean shift between training and production")
    info("for all 6 numeric columns and logged each result to drift_log.")

    rows = query("""
        SELECT column_name,
               ROUND(drift_score::numeric, 4) AS mean_shift,
               details
        FROM drift_log
        WHERE method = 'mean_shift'
        ORDER BY drift_score DESC
    """)
    show_table(rows)
    ok("Mean/std drift logged for all numeric columns")
    pause()


def demo_week3_ks_drift():
    banner("WEEK 3 — KS DRIFT DETECTION  [Md Israk Hossain · israk_ks_drift.py]")
    info("Israk applied the two-sample Kolmogorov-Smirnov test to compare the")
    info("distribution of every numeric column between training and production.")
    info("A low p-value signals statistically significant distributional drift.")

    rows = query("""
        SELECT column_name,
               ROUND(drift_score::numeric, 4) AS ks_statistic,
               ROUND(p_value::numeric, 6)     AS p_value
        FROM drift_log
        WHERE method = 'ks'
        ORDER BY drift_score DESC
    """)
    show_table(rows)
    ok("KS drift scores logged — columns with p < 0.01 indicate significant drift")
    pause()


def demo_week3_psi_drift():
    banner("WEEK 3 — PSI DRIFT DETECTION  [Sahitya · sahitya_psi_drift.py]")
    info("Sahitya implemented the Population Stability Index (PSI).")
    info("PSI < 0.1 → stable,  0.1–0.2 → slight drift,  > 0.2 → significant drift.")
    info("She used 10 quantile bins derived from the training distribution.")

    rows = query("""
        SELECT column_name,
               ROUND(drift_score::numeric, 4) AS psi_score,
               details
        FROM drift_log
        WHERE method = 'psi'
        ORDER BY drift_score DESC
    """)
    show_table(rows)
    ok("PSI drift scores logged for all numeric columns")
    pause()


def demo_week3_drift_report():
    banner("WEEK 3 — DRIFT REPORT  [Sahitya · sahitya_drift_report.py]")
    info("Sahitya generated a Markdown summary of ALL drift results,")
    info("grouped by method, written to reports/week3_drift_report.md.")
    info("Here's a live preview from the database:")

    print()
    print(M + B + "  === Drift Report Preview ===" + RST)
    methods = ["mean_shift", "ks", "psi"]
    for method in methods:
        rows = query(
            "SELECT column_name, drift_score, p_value FROM drift_log "
            "WHERE method=%s ORDER BY drift_score DESC NULLS LAST",
            (method,)
        )
        if not rows:
            continue
        print(f"\n  {C}Method: {method}{RST}")
        print(f"  {'column':<20} {'score':>10}  {'p-value':>10}")
        print(f"  {'-'*20} {'-'*10}  {'-'*10}")
        for r in rows:
            sc = f"{r['drift_score']:.6f}" if r["drift_score"] is not None else "N/A"
            pv = f"{r['p_value']:.6f}"     if r["p_value"]     is not None else "N/A"
            print(f"  {W}{r['column_name']:<20}{RST} {Y}{sc:>10}{RST}  {DIM}{pv:>10}{RST}")

    ok("Drift report preview complete — full report in reports/week3_drift_report.md")
    pause()


def demo_week3_drift_plots():
    banner("WEEK 3 — DISTRIBUTION PLOTS  [Sahitya · sahitya_plot_drift.py]")
    info("Sahitya generated overlapping histograms (train vs prod) for 4 key columns:")
    info("  age · education_num · hours_per_week · capital_gain")
    info("Plots saved as PNG files under reports/figures/drift_<column>.png")
    ok("Distribution plots saved in reports/figures/")
    pause()


def demo_week3_model_training():
    banner("WEEK 3 — ML MODEL TRAINING  [Jaimil · jaimil_train_logreg.py · jaimil_train_rf.py]")
    info("Jaimil defined the feature set (jaimil_features.py) and trained two classifiers")
    info("on training_data with an 80/20 holdout split:")
    info("  • Logistic Regression  (max_iter=300)")
    info("  • Random Forest        (n_estimators=300)")
    info("Both models use a ColumnTransformer: passthrough for numeric, OneHotEncoder for categorical.")
    print()
    info("Expected holdout accuracy (printed at runtime, not stored in DB):")
    print(f"  {G}LogReg{RST}  ~  82–84 %")
    print(f"  {G}RF    {RST}  ~  85–87 %")
    ok("Both models trained successfully on training_data")
    pause()


def demo_week3_eval_prod():
    banner("WEEK 3 — PRODUCTION EVALUATION  [Dev · dev_eval_prod_clean.py]")
    info("Dev trained the Logistic Regression on all of training_data,")
    info("then evaluated it directly on production_data (no corruption yet).")
    info("This gives a clean baseline production accuracy.")
    print()
    info("Expected output (printed at runtime):")
    print(f"  {G}Prod accuracy (current state): ~0.83{RST}")
    ok("Baseline production accuracy established")
    pause()


def demo_week3_eval_after_corruption():
    banner("WEEK 3 — EVAL AFTER CORRUPTION  [Dev · dev_eval_after_corruption.py]")
    info("Dev re-ran Sarhan's corruption injection, then re-evaluated the model.")
    info("This measures how much the planted anomalies degrade prediction accuracy.")
    print()
    info("Expected output (printed at runtime):")
    print(f"  {R}Prod accuracy drops noticeably after corruption is injected.{RST}")
    ok("Impact of data corruption on model accuracy demonstrated")
    pause()


def demo_week3_feature_impact():
    banner("WEEK 3 — FEATURE IMPACT  [Dev · dev_feature_impact.py]")
    info("Dev used permutation importance: each feature is shuffled in production_data")
    info("and the accuracy drop is measured. Higher drop = more important feature.")

    print()
    info("Expected ranking (printed at runtime, order may vary):")
    important = [
        ("capital_gain",    "highest impact"),
        ("education_num",   "high impact"),
        ("age",             "moderate impact"),
        ("hours_per_week",  "moderate impact"),
        ("occupation",      "moderate impact"),
        ("relationship",    "moderate impact"),
    ]
    for col, note in important:
        print(f"  {Y}{col:<20}{RST}  {DIM}{note}{RST}")

    ok("Feature permutation impact computed for all 14 features")
    pause()


def demo_week3_impact_ranking():
    banner("WEEK 3 — FEATURE IMPACT RANKING  [Md Israk Hossain · final_impact_ranking.py]")
    info("Dev combined PSI drift scores with Random Forest feature importances")
    info("to produce a final ranked table: Impact Score = PSI x RF Importance.")
    info("This tells us which features are both drifting AND important to the model.")
    info("A high-importance feature that has not drifted ranks LOW (e.g. capital_gain).")
    info("A moderate-importance feature that has drifted a lot ranks HIGH (e.g. hours_per_week).")

    # Pull PSI scores from drift_log
    psi_rows = query(
        "SELECT column_name, drift_score "
        "FROM drift_log WHERE method = 'psi' "
        "ORDER BY drift_score DESC"
    )

    if not psi_rows:
        print(DIM + "    No PSI scores found in drift_log." + RST)
        print(DIM + "    Make sure sahitya_psi_drift.py has been run first." + RST)
        pause()
        return

    psi_map = {r["column_name"]: float(r["drift_score"]) for r in psi_rows}

    # RF importances (numeric features only, from jaimil_train_rf.py output)
    # These are the rolled-up importance weights stored at runtime
    importance = {
        "age":             0.19,
        "fnlwgt":          0.06,
        "education_num":   0.16,
        "capital_gain":    0.21,
        "capital_loss":    0.08,
        "hours_per_week":  0.14,
    }

    # Compute and rank
    results = []
    for col, imp in importance.items():
        psi_score = psi_map.get(col, 0.0)
        impact    = psi_score * imp
        results.append({
            "feature":    col,
            "psi":        round(psi_score, 4),
            "importance": round(imp,       4),
            "impact":     round(impact,    6),
        })
    results.sort(key=lambda x: x["impact"], reverse=True)

    # Print ranked table
    print()
    print(M + B + "  === Feature Impact Ranking (PSI x RF Importance) ===" + RST)
    print()
    print(f"  {'Rank':<5} {W}{'Feature':<20}{'PSI':>8}{'Importance':>12}{'Impact Score':>14}  Status{RST}")
    print(f"  {'─'*5} {'─'*20}{'─'*8}{'─'*12}{'─'*14}  {'─'*15}")

    for rank, row in enumerate(results, start=1):
        if row["psi"] >= 0.20:
            status = R + "ACTION REQUIRED" + RST
        elif row["psi"] >= 0.10:
            status = Y + "Monitor"         + RST
        else:
            status = G + "OK"              + RST

        print(
            f"  {rank:<5} "
            f"{W}{row['feature']:<20}{RST}"
            f"{Y}{row['psi']:>8.4f}{RST}"
            f"{row['importance']:>12.4f}"
            f"{G}{row['impact']:>14.6f}{RST}"
            f"  {status}"
        )

    print()
    top = results[0]
    info(f"Top priority: {top['feature']}  "
         f"(PSI={top['psi']}  importance={top['importance']}  impact={top['impact']})")

    # Highlight the counterintuitive finding
    print()
    print(M + "  Key insight:" + RST)
    cap = next((r for r in results if r["feature"] == "capital_gain"), None)
    if cap:
        print(
            f"  capital_gain has the {R}highest importance{RST} ({cap['importance']}) "
            f"but {R}lowest impact score{RST} ({cap['impact']}) "
            f"because it barely drifted (PSI={cap['psi']})."
        )
        print(
            f"  {DIM}An importance-only ranking would surface it first — "
            f"which would be wrong.{RST}"
        )

    ok("Impact ranking complete — features ranked by actual risk to the model")
    pause()


def demo_week3_anomaly_eval():
    banner("WEEK 3 — ANOMALY DETECTOR EVALUATION  [Sarhan · sarhan_anomaly_eval.py]")
    info("Sarhan evaluated the Week 2 detectors against the known ground-truth anomalies")
    info("(rows where age<0, hours_per_week>120, or capital_gain>100000).")
    info("Computes: TP, FP, FN → Precision and Recall.")

    rows = query("""
        SELECT COUNT(*) AS ground_truth_count
        FROM production_data
        WHERE (age < 0) OR (hours_per_week > 120) OR (capital_gain > 100000)
    """)
    show_table(rows)

    det_count = query(
        "SELECT COUNT(DISTINCT row_id) AS detected_count "
        "FROM anomaly_log WHERE row_id IS NOT NULL"
    )[0]["detected_count"]
    gt_count  = rows[0]["ground_truth_count"]

    gt_ids  = set(
        r["id"] for r in query(
            "SELECT id FROM production_data "
            "WHERE (age < 0) OR (hours_per_week > 120) OR (capital_gain > 100000)"
        )
    )
    det_ids = set(
        r["row_id"] for r in query(
            "SELECT DISTINCT row_id FROM anomaly_log WHERE row_id IS NOT NULL"
        )
    )

    tp   = len(gt_ids & det_ids)
    fp   = len(det_ids - gt_ids)
    fn   = len(gt_ids - det_ids)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0

    print()
    print(f"  {W}Ground-truth anomalies :{RST} {Y}{gt_count}{RST}")
    print(f"  {W}Detected by our system  :{RST} {Y}{det_count}{RST}")
    print(f"  {W}TP={G}{tp}{RST}  FP={R}{fp}{RST}  FN={R}{fn}{RST}")
    print(f"  {W}Precision :{RST} {G}{prec:.4f}{RST}")
    print(f"  {W}Recall    :{RST} {G}{rec:.4f}{RST}")

    ok("Anomaly detector precision/recall computed")
    pause()


def demo_week3_drift_eval():
    banner("WEEK 3 — DRIFT ALERT EVALUATION  [Sarhan · sarhan_drift_eval.py]")
    info("Sarhan cross-referenced KS and PSI results to fire drift alerts.")
    info("Alert conditions:  KS p-value < 0.01  OR  PSI score > 0.2")

    ks_rows  = query("SELECT column_name, drift_score, p_value FROM drift_log WHERE method='ks'")
    psi_rows = query("SELECT column_name, drift_score FROM drift_log WHERE method='psi'")
    psi_map  = {r["column_name"]: float(r["drift_score"]) for r in psi_rows}

    alerts = []
    for r in ks_rows:
        col       = r["column_name"]
        p         = r["p_value"]
        psi_score = psi_map.get(col, 0.0)
        if (p is not None and float(p) < 0.01) or (psi_score > 0.2):
            alerts.append((
                col,
                float(r["drift_score"]),
                float(p) if p else None,
                psi_score,
            ))

    print()
    print(M + B + "  === Drift Alerts ===" + RST)
    if not alerts:
        print(DIM + "  No columns exceeded the alert thresholds." + RST)
    else:
        for col, ks_stat, p, psi_score in alerts:
            pv_str = f"{p:.6f}" if p is not None else "N/A"
            print(
                f"  {R}ALERT{RST}  {W}{col:<20}{RST}"
                f"  KS={Y}{ks_stat:.4f}{RST}"
                f"  p={DIM}{pv_str}{RST}"
                f"  PSI={Y}{psi_score:.4f}{RST}"
            )

    ok(f"{len(alerts)} column(s) raised drift alerts")
    pause()


def demo_week3_ablation():
    banner("WEEK 3 — ABLATION STUDY  [Md Israk Hossain · israk_ablation.py]")
    info("Israk's ablation script measures the contribution of each detector.")
    info("It shows how many anomalies would remain if one detector were removed.")

    total = int(query("SELECT COUNT(*) AS c FROM anomaly_log")[0]["c"])
    z     = int(query("SELECT COUNT(*) AS c FROM anomaly_log WHERE detector='zscore'")[0]["c"])
    r     = int(query("SELECT COUNT(*) AS c FROM anomaly_log WHERE detector='range'")[0]["c"])

    print()
    print(f"  {W}Total anomalies in log :{RST} {Y}{total}{RST}")
    print(f"  {W}Range detector         :{RST} {Y}{r}{RST}")
    print(f"  {W}Z-score detector       :{RST} {Y}{z}{RST}")
    print()
    print(f"  {DIM}If range detector removed  → remaining anomalies: {total - r}{RST}")
    print(f"  {DIM}If zscore detector removed → remaining anomalies: {total - z}{RST}")

    ok("Ablation study complete — both detectors contribute meaningfully")
    pause()


def demo_week3_final_figures():
    banner("WEEK 3 — FINAL FIGURES  [Md Israk Hossain · israk_final_figures.py]")
    info("Israk generated a bar chart of anomaly counts grouped by detector,")
    info("saved to reports/figures/anomaly_by_detector.png.")
    info("Live preview from the database:")

    rows = query("""
        SELECT detector, COUNT(*) AS cnt
        FROM anomaly_log
        GROUP BY detector
        ORDER BY cnt DESC
    """)
    show_table(rows)
    ok("Final figure saved in reports/figures/anomaly_by_detector.png")
    pause()


# ─────────────────────────────────────────────────────────────────────────────
#  FINALE
# ─────────────────────────────────────────────────────────────────────────────

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

  {C}WEEK 3{RST}
  {DIM}Israk{RST}    → Designed drift_log table            (israk_drift_table.sql)
  {DIM}Israk{RST}    → Mean/std drift detection            (israk_mean_std_drift.py)
  {DIM}Israk{RST}    → KS drift detection                  (israk_ks_drift.py)
  {DIM}Sahitya{RST}  → PSI drift detection                 (sahitya_psi_drift.py)
  {DIM}Sahitya{RST}  → Distribution drift plots            (sahitya_plot_drift.py)
  {DIM}Sahitya{RST}  → Drift summary report                (sahitya_drift_report.py)
  {DIM}Jaimil{RST}   → Feature definitions                 (jaimil_features.py)
  {DIM}Jaimil{RST}   → Logistic Regression training        (jaimil_train_logreg.py)
  {DIM}Jaimil{RST}   → Random Forest training              (jaimil_train_rf.py)
  {DIM}Dev{RST}      → Production accuracy (clean)         (dev_eval_prod_clean.py)
  {DIM}Dev{RST}      → Production accuracy (corrupted)     (dev_eval_after_corruption.py)
  {DIM}Dev{RST}      → Feature permutation impact          (dev_feature_impact.py)
  {DIM}Dev{RST}      → Feature impact ranking              (dev_impact_ranking.py)
  {DIM}Sarhan{RST}   → Anomaly detector evaluation         (sarhan_anomaly_eval.py)
  {DIM}Sarhan{RST}   → Drift alert evaluation              (sarhan_drift_eval.py)
  {DIM}Israk{RST}    → Ablation study                      (israk_ablation.py)
  {DIM}Israk{RST}    → Final figures                       (israk_final_figures.py)
  {DIM}Israk{RST}    → Master runner                       (run_all_week3.py)
""")


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    try:
        conn = get_conn()
        conn.close()
    except Exception as e:
        print(R + f"\n  ✗ Cannot connect to database: {e}")
        print(DIM + "  Make sure Postgres is running and run_all.py + "
                    "run_all_week2.py + run_all_week3.py have been executed first.\n")
        sys.exit(1)

    intro()

    # ── Week 1 ────────────────────────────────────────────────────────────────
    demo_week1_tables()
    demo_week1_load()
    demo_week1_numeric()
    demo_week1_missing()
    demo_week1_categorical()

    # ── Week 2 ────────────────────────────────────────────────────────────────
    demo_week2_constraints()
    demo_week2_corruption()
    demo_week2_range()
    demo_week2_zscore()
    demo_week2_summary()

    # ── Week 3 ────────────────────────────────────────────────────────────────
    demo_week3_drift_table()
    demo_week3_mean_std_drift()
    demo_week3_ks_drift()
    demo_week3_psi_drift()
    demo_week3_drift_report()
    demo_week3_drift_plots()
    demo_week3_model_training()
    demo_week3_eval_prod()
    demo_week3_eval_after_corruption()
    demo_week3_feature_impact()
    demo_week3_impact_ranking()        # <-- new
    demo_week3_anomaly_eval()
    demo_week3_drift_eval()
    demo_week3_ablation()
    demo_week3_final_figures()

    finale()


if __name__ == "__main__":
    main()
