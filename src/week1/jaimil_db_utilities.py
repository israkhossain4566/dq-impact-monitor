import os 

import psycopg2 

from psycopg2.extras import RealDictCursor 

 

def get_conn(): 

    return psycopg2.connect( 

        host=os.getenv("DB_HOST", "localhost"), 

        port=int(os.getenv("DB_PORT", "5432")), 

        dbname=os.getenv("DB_NAME", "dqdb"), 

        user=os.getenv("DB_USER", "dq"), 

        password=os.getenv("DB_PASS", "dqpass"), 

    ) 

 

def fetchall(query: str, params=None): 

    with get_conn() as conn: 

        with conn.cursor(cursor_factory=RealDictCursor) as cur: 

            cur.execute(query, params) 

            return cur.fetchall() 

 

def execute(query: str, params=None): 

    with get_conn() as conn: 

        with conn.cursor() as cur: 

            cur.execute(query, params) 

        conn.commit() 
