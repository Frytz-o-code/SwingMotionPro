# app/pages/login.py

import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_mantine_components as dmc
from flask import session
from app.auth import login_user

dash.register_page(__name__, path="/login", name="Login")

layout = dmc.Container([
    dmc.Title("Login", order=2, mb="md"),
    dmc.TextInput(id="login-email", label="E-Mail", required=True),
    dmc.PasswordInput(id="login-password", label="Passwort", required=True, mt="sm"),
    dmc.Button("Einloggen", id="login-button", mt="md"),
    dcc.Location(id="login-redirect", refresh=True),
    dmc.Text(id="login-message", c="red", mt="md")
], size="xs", mt=50)