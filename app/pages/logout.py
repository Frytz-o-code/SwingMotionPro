# app/pages/logout.py

import dash
from dash import dcc
from app.auth import logout_user
import dash_mantine_components as dmc

import dash
dash.register_page(__name__, path="/logout", name="Logout")

def layout():
    logout_user()  # Session beenden

    return dmc.Container([
        dmc.Title("Abmeldung", order=2, mb="md"),
        dmc.Text("Du wirst nun abgemeldet..."),
        dcc.Location(href="/login", id="logout-redirect", refresh=True)
    ])