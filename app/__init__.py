import os
from flask import Flask
import dash
from dash import dcc, html
from flask_session import Session
import dash_mantine_components as dmc

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
        external_stylesheets=dmc.styles.ALL  # Mantine-Styles korrekt einbinden
    )

    # Navigation + Seiten
    app.layout = dmc.MantineProvider(
        children=[
            dcc.Location(id="url"),
            dash.page_container
        ]
    )

    return