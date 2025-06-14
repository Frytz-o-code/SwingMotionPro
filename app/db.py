from app.config import DATABASE_URL
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import session

#DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


#def get_db_connection():
#    return psycopg2.connect(os.environ["DATABASE_URL"])

def get_current_user_id():
    return session.get("user_id")

def load_users():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, role FROM users ORDER BY id")
            return cur.fetchall()