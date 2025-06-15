import dash
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session
from dash.exceptions import PreventUpdate
import base64
import pandas as pd
import io

from app.db import get_db_connection, get_current_user_id
from app.utils.id_helpers import make_id_factory  # ID-Generator importieren

dash.register_page(__name__, path="/upload", name="Upload", icon="tabler:upload")
make_id = make_id_factory(__name__)  # e.g. "pages-upload"

# Layout als Funktion, damit Session geprüft wird
def layout():
    if "user_id" not in session:
        return html.Div([
            dmc.Alert(
                title="Nicht eingeloggt",
                children="🔒 Zugriff verweigert – bitte zuerst einloggen.",
                color="red"
            )
        ])

    return dmc.Stack([
        dmc.Title("📤 Golfdaten hochladen", order=2),
        dcc.Upload(
            id=make_id("upload-data"),
            children=dmc.Button(
                "CSV-Datei auswählen",
                leftSection=DashIconify(icon="tabler:upload", width=20)
            ),
            multiple=False,
            accept=".csv"
        ),
        html.Div(id=make_id("upload-feedback"))
    ])

@callback(
    Output(make_id("upload-feedback"), "children"),
    Input(make_id("upload-data"), "contents"),
    State(make_id("upload-data"), "filename"),
    prevent_initial_call=True
)
def handle_upload(contents, filename):
    if "user_id" not in session:
        return dmc.Alert(title="🔒 Nicht eingeloggt – Upload nicht möglich.", color="red")

    if contents is None:
        raise PreventUpdate

    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        user_id = get_current_user_id()
        conn = get_db_connection()
        cur = conn.cursor()

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO golf_shots (
                    user_id, datum, schlaegerart, smash_factor, carry_distanz,
                    gesamtstrecke, ballgeschwindigkeit
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                user_id,
                row.get("Datum"),
                row.get("Schlägerart"),
                row.get("Smash_Factor"),
                row.get("CarryDistanz"),
                row.get("Gesamtstrecke"),
                row.get("Ballgeschwindigkeit"),
            ))

        conn.commit()
        cur.close()
        conn.close()

        return dmc.Alert(
            title="✅ Upload erfolgreich",
            children=f"{filename} wurde gespeichert.",
            color="green"
        )

    except Exception as e:
        return dmc.Alert(
            title="❌ Fehler beim Upload",
            children=str(e),
            color="red"
        )