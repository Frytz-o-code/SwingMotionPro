# app/auth.py
from app.config import DATABASE_URL
import os
import bcrypt
from flask import session, redirect, url_for, request
from .db import get_db_connection
from app.logging_config import get_logger
logger = get_logger(__name__)  # ergibt z. B. "app.pages.upload"


# Passwort-Hashing
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Passwortprüfung
def check_password(password: str, hash_: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash_.encode())

# Nutzer anhand von E-Mail aus DB holen
def get_user_by_email(email: str):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cur.fetchone()

# Nutzer-ID holen (aus Session)
def get_current_user():
    return session.get("user_id")

# Nutzerrolle holen
def get_user_role():
    return session.get("user_role")

# Login durchführen
def login_user(email: str, password: str) -> bool:
    user = get_user_by_email(email)
    logger.debug(user["password_hash"])
    if user and check_password(password, user["password_hash"]):
        session["user_id"] = str(user["id"])
        session["user_email"] = user["email"]
        session["user_role"] = user["role"]
        return True
    return False

# Logout
def logout_user():
    session.clear()

# Zugriffsschutz: Login erforderlich
def require_login():
    if not get_current_user():
        return redirect("/login")

# Zugriffsschutz: Nur Admin
def require_admin():
    if get_user_role() != "admin":
        return redirect("/unauthorized")
    
    