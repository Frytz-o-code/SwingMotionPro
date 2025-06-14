# scripts/drop_all.py

import os
import psycopg2
import sys

def drop_all():
    env = os.environ.get("ENV", "production")
    if env != "development":
        print("❌ Löschen der Datenbank ist nur in der Development-Umgebung erlaubt. Aktuelle ENV:", env)
        sys.exit(1)

    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        print("⚠️  Lösche alle Tabelleninhalte …")
        cur.execute("""
            DROP TABLE IF EXISTS golf_shots;
            DROP TABLE IF EXISTS users;
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Alle Tabellen erfolgreich gelöscht.")
    except Exception as e:
        print("❌ Fehler beim Löschen:", e)

if __name__ == "__main__":
    drop_all()