# app/utils/csv_upload_handler.py

import base64
import io
import pandas as pd
from dash.exceptions import PreventUpdate
from dash import html
import dash_mantine_components as dmc

from app.utils.csv_format_mappings import csv_format_registry


def parse_and_transform_csv(contents: str, format_key: str) -> pd.DataFrame:
    if format_key not in csv_format_registry:
        raise ValueError(f"Unbekanntes Format: {format_key}")

    format_conf = csv_format_registry[format_key]

    # CSV-Daten dekodieren
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        decoded_str = decoded.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Fehler beim Dekodieren: {e}")

    # DataFrame laden
    try:
        df = pd.read_csv(io.StringIO(decoded_str))
    except Exception as e:
        raise ValueError(f"Fehler beim Einlesen der CSV: {e}")

    # Spalten-Mapping anwenden
    column_map = format_conf.get("column_map", {})
    df = df.rename(columns=column_map)

    # Pflichtspalten prüfen
    required_cols = ["Datum", "Schlägerart", "Smash_Factor", "CarryDistanz", "Gesamtstrecke", "Ballgeschwindigkeit"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Fehlende Spalten nach Umbenennung: {', '.join(missing)}")

    # Einheitenkonvertierung
    conversions = format_conf.get("unit_conversion", {})
    for col, func in conversions.items():
        try:
            df[col] = df[col].apply(func)
        except Exception as e:
            raise ValueError(f"Fehler bei Umrechnung von '{col}': {e}")

    # Datum parsen
    date_format = format_conf.get("date_format")
    try:
        df["Datum"] = pd.to_datetime(df["Datum"], format=date_format)
    except Exception as e:
        raise ValueError(f"Fehler beim Parsen der Datumsangaben: {e}")

    return df