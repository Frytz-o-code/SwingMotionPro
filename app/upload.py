from dash import html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
import base64
import pandas as pd
import io
import psycopg2
from flask import session
import dash
from config import DATABASE_URL

from app.db import get_current_user_id, get_db_connection
from app.utils.csv_format_mappings import csv_format_registry

# Dash-Seite registrieren
dash.register_page(__name__, path="/upload", name="CSV Upload", icon="tabler:upload")

# Layout-Funktion (verhindert Zugriff auf session beim Import!)
def layout():
    if "user_id" not in session:
        return html.Div([
            dmc.Alert("🔒 Zugriff verweigert – bitte zuerst einloggen.", color="red", title="Nicht eingeloggt")
        ])
    
    return dmc.Stack([
        dmc.Title("📤 Golfdaten hochladen", order=2),
        dmc.Select(
            id="csv-format",
            label="CSV-Format wählen",
            data=[{"value": k, "label": v["label"]} for k, v in csv_format_registry.items()],
            value="deutsch_csv"
        ),
        dcc.Upload(
            id="upload-data",
            children=dmc.Button("CSV-Datei auswählen", leftIcon=dmc.ThemeIcon("tabler:upload", size=20)),
            multiple=False,
            accept=".csv"
        ),
        html.Div(id="upload-feedback")
    ])

# Callback zur Verarbeitung des Uploads
@callback(
    Output("upload-feedback", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("csv-format", "value"),
    prevent_initial_call=True
)
def handle_upload(contents, filename, csv_format_key):
    if "user_id" not in session:
        return dmc.Alert("🔒 Nicht eingeloggt – Upload nicht möglich.", color="red")

    if not contents or not csv_format_key:
        raise PreventUpdate

    try:
        format_def = csv_format_registry[csv_format_key]
        column_map = format_def["column_map"]
        unit_conversion = format_def["unit_conversion"]
        date_format = format_def.get("date_format")

        # CSV einlesen
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

        # Spalten umbenennen
        if column_map:
            df = df.rename(columns=column_map)

        # Einheiten umrechnen
        for col, func in unit_conversion.items():
            if col in df.columns:
                df[col] = df[col].apply(func)

        # Datum parsen
        if "Datum" in df.columns and date_format:
            df["Datum"] = pd.to_datetime(df["Datum"], format=date_format, errors="coerce")

        # Speichern in Datenbank
        user_id = get_current_user_id()
        conn = get_db_connection()
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO golf_shots (
                    user_id, datum, schlaegerart, smash_factor, carry_distanz,
                    gesamtstrecke, ballgeschwindigkeit
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, [
                user_id,
                row.get("Datum"),
                row.get("Schlägerart"),
                row.get("Smash_Factor"),
                row.get("CarryDistanz"),
                row.get("Gesamtstrecke"),
                row.get("Ballgeschwindigkeit"),
            ])
        conn.commit()
        cur.close()
        conn.close()

        return dmc.Alert(title="✅ Upload erfolgreich", children=f"{filename} wurde gespeichert.", color="green")

    except Exception as e:
        return dmc.Alert(title="❌ Fehler beim Upload", children=str(e), color="red")