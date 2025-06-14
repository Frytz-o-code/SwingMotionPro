# pages/upload.py

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from flask import session
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path="/upload", name="Upload", icon="tabler:upload")

layout = (
    html.Div([
        dmc.Alert("🔒 Zugriff verweigert – bitte zuerst einloggen.", color="red", title="Nicht eingeloggt")
    ])
    if "user_id" not in session else
    dmc.Stack([
        dmc.Title("📤 Golfdaten hochladen", order=2),
        dcc.Upload(
            id="upload-data",
            children=dmc.Button("CSV-Datei auswählen", leftIcon=dmc.ThemeIcon("tabler:upload", size=20)),
            multiple=False,
            accept=".csv"
        ),
        html.Div(id="upload-feedback")
    ])
)

@callback(
    Output("upload-feedback", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def handle_upload(contents, filename):
    if "user_id" not in session:
        return dmc.Alert("🔒 Nicht eingeloggt – Upload nicht möglich.", color="red")

    if contents is None:
        raise PreventUpdate

    try:
        # ⬇️ Base64-dekodieren und mit pandas einlesen
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # ⬇️ Benutzer-ID abrufen
        user_id = get_current_user_id()

        # ⬇️ Verbindung zur DB
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
