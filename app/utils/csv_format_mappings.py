csv_format_registry = {
    "deutsch_csv": {
        "label": "CSV mit deutschen Überschriften",
        "column_map": {
            "Datum": "shot_time",
            "Spieler": "csv_username",
            "Schlägerart": "club_type",
            "Smash Factor": "smash_factor",
            "Carry-Distanz": "carry_distance",
            "Gesamtstrecke": "total_distance",
            "Ballgeschwindigkeit": "ball_speed_kph",
        },
        "unit_conversion": {},  # Optional bei Bedarf
        "date_format": "%Y-%m-%d %H:%M:%S %z"
    },

    "flightscope": {
        "label": "FlightScope Standard (EN)",
        "column_map": {
            "Shot Date/Time": "shot_time",
            "Player": "csv_username",
            "Club Type": "club_type",
            "Smash Factor": "smash_factor",
            "Carry Distance": "carry_distance",
            "Total Distance": "total_distance",
            "Ball Speed": "ball_speed_kph"
        },
        "unit_conversion": {
            "ball_speed_kph": lambda x: x * 1.60934  # mph → km/h
        },
        "date_format": "%Y-%m-%d %H:%M:%S %z"
    },
}