# app/pages/upload.py

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session
from dash.exceptions import PreventUpdate
import base64
import pandas as pd
import io
from datetime import datetime
from app.logging_config import get_logger

from app.db import get_db_connection, get_current_user_id
from app.utils.id_helpers import make_id_factory
from app.utils.csv_format_mappings import csv_format_registry

logger = get_logger(__name__)
logger.debug("✅ upload.py: Logger funktioniert")

dash.register_page(__name__, path="/upload", name="Upload", icon="tabler:upload")
make_id = make_id_factory(__name__)

def layout():
    if "user_id" not in session:
        logger.warning("⚠️ Upload-Zugriff ohne Session")
        return html.Div([
            dmc.Alert(
                title="Nicht eingeloggt",
                children="🔒 Zugriff verweigert – bitte zuerst einloggen.",
                color="red"
            )
        ])

    return dmc.Stack([
        dmc.Title("📤 Golfdaten hochladen", order=2),
        dmc.Select(
            label="Format auswählen",
            id=make_id("format-select"),
            data=[{"label": f["label"], "value": key} for key, f in csv_format_registry.items()],
            value="deutsch_csv",
            clearable=False,
            mb="md"
        ),
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
    State(make_id("format-select"), "value"),
    prevent_initial_call=True
)
def handle_upload(contents, filename, selected_format):
    if "user_id" not in session:
        return dmc.Alert(title="🔒 Nicht eingeloggt – Upload nicht möglich.", color="red")

    if contents is None:
        raise PreventUpdate

    try:
        logger.info(f"📁 Upload gestartet: {filename} (Format: {selected_format})")

        # --- CSV lesen ---
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        logger.debug(f"📊 Originalspalten: {df.columns.tolist()}")

        # --- Formatregeln anwenden ---
        fmt = csv_format_registry[selected_format]
        col_map = fmt.get("column_map", {})
        unit_conv = fmt.get("unit_conversion", {})
        date_fmt = fmt.get("date_format", "%Y-%m-%d %H:%M:%S %z")
        date_col = col_map.get("Datum", "shot_time")  # Fallback, falls "Datum" nicht gemappt ist

        # Spalten umbenennen
        if col_map:
            df = df.rename(columns=col_map)

        logger.debug(f"📊 Nach Mapping: {df.columns.tolist()}")

        # Einheiten umrechnen
        for col, func in unit_conv.items():
            if col in df.columns:
                df[col] = df[col].apply(func)

        # Zeitspalte prüfen und parsen
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], format=date_fmt, errors="coerce")
            df = df[df[date_col].notna()]
        else:
            logger.warning(f"⚠️ Zeitspalte '{date_col}' nicht gefunden.")
            return dmc.Alert(title="❌ Fehler", children=f"Spalte '{date_col}' fehlt in der Datei.", color="red")

        logger.info(f"📈 {len(df)} gültige Zeilen nach Parsing")

        # --- DB speichern ---
        user_id = get_current_user_id()
        conn = get_db_connection()
        cur = conn.cursor()

        for _, row in df.iterrows():
            logger.debug(f"⛳ INSERT: {row.to_dict()}")
            cur.execute("""
                INSERT INTO golf_shots (
                    user_id, csv_username, shot_time, club_type, smash_factor,
                    carry_distance, total_distance, ball_speed_kph
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                
                user_id,
                row.get("csv_username"),
                row.get("shot_time"),
                row.get("club_type"),
                row.get("smash_factor"),
                row.get("carry_distance"),
                row.get("total_distance"),
                row.get("ball_speed_kph"),
            ))

        conn.commit()
        cur.close()
        conn.close()

        logger.info(f"✅ Upload abgeschlossen: {filename}")
        return dmc.Alert(title="✅ Upload erfolgreich", children=f"{filename} wurde gespeichert.", color="green")

    except Exception as e:
        logger.exception("❌ Fehler beim Upload")
        return dmc.Alert(title="❌ Fehler beim Upload", children=str(e), color="red")