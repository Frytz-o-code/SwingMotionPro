# app/pages/login.py

import dash
from dash import html, dcc, Input, Output, State, ctx, callback
import dash_mantine_components as dmc
from flask import session
from app.auth import login_user
from app.logging_config import get_logger
from app.utils.id_helpers import make_id_factory
from dash.exceptions import PreventUpdate

# ID-Factory für diese Seite
make_id = make_id_factory("login")

logger = get_logger(__name__)
dash.register_page(__name__, path="/login", name="Login")

layout = dmc.Container(
    children=[
        dmc.Title("Login", order=2, mb="md"),
        dmc.TextInput(id=make_id("email"), label="E-Mail", required=True),
        dmc.PasswordInput(id=make_id("password"), label="Passwort", required=True, mt="sm"),
        dmc.Button("Einloggen", id=make_id("button"), mt="md"),
        dcc.Location(id=make_id("redirect"), refresh=True),
        dmc.Text(id=make_id("message"), children="", c="red", mt="md")
    ],
    size="xs",
    mt=50
)

@callback(
    Output(make_id("message"), "children"),
    Output(make_id("redirect"), "href"),
    Input(make_id("button"), "n_clicks"),
    State(make_id("email"), "value"),
    State(make_id("password"), "value"),
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not email or not password:
        logger.info("Login attempt with missing fields.")
        return "Bitte E-Mail und Passwort eingeben.", dash.no_update

    logger.info(f"Login attempt for: {email}")
    success = login_user(email, password)

    if success:
        logger.info(f"Login erfolgreich: {email}")
        return "", "/"
    else:
        logger.warning(f"Login fehlgeschlagen für: {email}")
        return "❌ Login fehlgeschlagen. Bitte prüfen Sie Ihre Eingaben.", dash.no_update