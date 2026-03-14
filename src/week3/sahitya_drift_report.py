from src.week1.jaimil_db_utilities import fetchall 

 

OUT = "reports/week3_drift_report.md" 

 

def run(): 

    rows = fetchall(""" 

        SELECT method, column_name, drift_score, p_value, details 

        FROM drift_log 

        ORDER BY method, drift_score DESC NULLS LAST; 

    """) 

    lines = [] 

    lines.append("# Week 3 Drift Report\n") 

    lines.append("This report summarizes drift scores between training and production.\n\n") 

    curr = None 

    for r in rows: 

        if r["method"] != curr: 

            curr = r["method"] 

            lines.append(f"## Method: {curr}\n") 

            lines.append("| column | score | p-value |\n|---|---:|---:|\n") 

        pv = "" if r["p_value"] is None else f"{r['p_value']:.6f}" 

        sc = "" if r["drift_score"] is None else f"{r['drift_score']:.6f}" 

        lines.append(f"| {r['column_name']} | {sc} | {pv} |\n") 

    with open(OUT, "w", encoding="utf-8") as f: 

        f.writelines(lines) 

    print(f"wrote {OUT}") 

 

if __name__ == "__main__": 

    run() 