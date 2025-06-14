# app/pages/logout.py

import dash
from dash import dcc, Output, Input
import dash_mantine_components as dmc
from flask import session
from app.auth import logout_user

dash.register_page(__name__, path="/logout", name="Logout")

layout = dmc.Container([
    dmc.Title(children="Abmeldung", order=2, mb="md"),
    dmc.Text(children="Du wirst nun abgemeldet..."),
    dcc.Location(id="logout-redirect", refresh=True)
])
from dash import callback

@callback(
    Output("logout-redirect", "href"),
    Input("logout-redirect", "pathname"),  # wird direkt beim Aufruf ausgelöst
    prevent_initial_call=True
)
def do_logout(_):
    logout_user()
    return "/login"