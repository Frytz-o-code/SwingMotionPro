# scripts/init_db.py

import os
import psycopg2

SCHEMA_SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "schema", "schema.sql")

def load_schema():
    with open(SCHEMA_SQL_PATH, "r", encoding="utf-8") as f:
        return f.read()

def init_db():
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        print("🔄 Initialisiere Datenbank …")
        cur.execute(load_schema())
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Schema erfolgreich angewendet.")
    except Exception as e:
        print("❌ Fehler bei der Initialisierung:", e)

if __name__ == "__main__":
    init_db()