# app/utils/csv_format_mappings.py

csv_format_registry = {
    "deutsch_csv": {
        "label": "CSV mit deutschen Überschriften",
        "column_map": {},  # identisch mit deiner DB-Struktur
        "unit_conversion": {},
        "date_format": "%d.%m.%Y %H:%M:%S"
    },
    "flightscope": {
        "label": "FlightScope Standard (EN)",
        "column_map": {
            "Shot Date/Time": "Datum",
            "Club Type": "Schlägerart",
            "Smash Factor": "Smash_Factor",
            "Carry Distance": "CarryDistanz",
            "Total Distance": "Gesamtstrecke",
            "Ball Speed": "Ballgeschwindigkeit"
        },
        "unit_conversion": {
            "Ballgeschwindigkeit": lambda x: x * 1.60934,  # mph → km/h
        },
        "date_format": "%Y-%m-%d %H:%M:%S"
    },
    # Weitere Formate ergänzbar...
}