from flask import session

def is_logged_in():
    return "user_id" in session

def current_user_role():
    return session.get("user_role", None)

def current_user_email():
    return session.get("user_email", None)