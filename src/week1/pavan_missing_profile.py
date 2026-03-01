import psycopg2
from psycopg2 import sql

DB = {
    "host": "localhost",
    "database": "dqdb",
    "user": "dq",
    "password": "dqpass",
}

TABLES = ["training_data", "production_data"]

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS missing_profile (
    dataset        TEXT NOT NULL,
    column_name    TEXT NOT NULL,
    n              INTEGER NOT NULL,
    n_null         INTEGER NOT NULL,
    null_rate      DOUBLE PRECISION NOT NULL,
    computed_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (dataset, column_name)
);
"""

UPSERT_SQL = """
INSERT INTO missing_profile (dataset, column_name, n, n_null, null_rate, computed_at)
VALUES (%s, %s, %s, %s, %s, NOW())
ON CONFLICT (dataset, column_name)
DO UPDATE SET
    n = EXCLUDED.n,
    n_null = EXCLUDED.n_null,
    null_rate = EXCLUDED.null_rate,
    computed_at = NOW();
"""

def get_columns(cur, table_name: str) -> list[str]:
    cur.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema='public' AND table_name=%s
        ORDER BY ordinal_position;
        """,
        (table_name,),
    )
    return [r[0] for r in cur.fetchall()]

def compute_missing_for_column(cur, table_name: str, col: str) -> tuple[int, int, float]:
    q = sql.SQL("""
        SELECT
            COUNT(*)::int AS n,
            SUM(CASE WHEN {c} IS NULL THEN 1 ELSE 0 END)::int AS n_null
        FROM {t};
    """).format(
        c=sql.Identifier(col),
        t=sql.Identifier(table_name),
    )
    cur.execute(q)
    n, n_null = cur.fetchone()
    null_rate = (n_null / n) if n else 0.0
    return n, n_null, null_rate

def main() -> None:
    conn = psycopg2.connect(**DB)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(CREATE_TABLE_SQL)

    for t in TABLES:
        cols = get_columns(cur, t)
        for col in cols:
            n, n_null, null_rate = compute_missing_for_column(cur, t, col)
            cur.execute(UPSERT_SQL, (t, col, n, n_null, null_rate))
        print(f"Done missingness profile for {t} ({len(cols)} columns).")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()