# app/__init__.py

import os
from flask import Flask
import dash
from dash import dcc, html
from flask_session import Session

# Dash-Factory-Funktion
def create_dash_app():
    server = Flask(__name__)

    # Geheimschlüssel für Sessions
    server.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")
    
    # Serverseitige Session (optional)
    server.config["SESSION_TYPE"] = "filesystem"
    Session(server)

    # Dash-Anwendung initialisieren
    app = dash.Dash(
        __name__,
        server=server,
        suppress_callback_exceptions=True,
        use_pages=True,  # für Multipage
        external_stylesheets=["https://unpkg.com/@mantine/ds@latest/styles.css"]
    )

    # Navigation + Seiten
    app.layout = html.Div([
        dcc.Location(id="url"),
        dash.page_container
    ])

    return app