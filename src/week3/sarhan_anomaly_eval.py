from src.week1.jaimil_db_utilities import fetchall

def run():
    gt = fetchall("""
        SELECT id FROM production_data
        WHERE (age < 0) OR (hours_per_week > 120) OR (capital_gain > 100000);
    """)
    gt_ids = set(r["id"] for r in gt)

    det = fetchall("SELECT DISTINCT row_id FROM anomaly_log WHERE row_id IS NOT NULL;")
    det_ids = set(r["row_id"] for r in det)

    tp = len(gt_ids & det_ids)
    fp = len(det_ids - gt_ids)
    fn = len(gt_ids - det_ids)

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0

    print("GT anomalies:", len(gt_ids))
    print("Detected:", len(det_ids))
    print(f"TP={tp} FP={fp} FN={fn}")
    print(f"Precision={prec:.4f} Recall={rec:.4f}")

if __name__ == "__main__":
    run()