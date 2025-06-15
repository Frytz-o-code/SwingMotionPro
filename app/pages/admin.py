# app/pages/admin.py

import dash
from dash import html, Output, Input, State, callback, ctx, no_update
import dash_mantine_components as dmc
from dash import ALL
from app.db import get_db_connection, load_users
from app.auth import get_user_role
from app.utils.id_helpers import make_id_factory
from app.logging_config import get_logger

logger = get_logger(__name__)
make_id = make_id_factory("admin")

dash.register_page(__name__, path="/admin", name="Adminbereich")

# --- Layout mit Nutzertabelle ---
def layout():
    if get_user_role() != "admin":
        return dmc.Alert(
            title="Nicht erlaubt",
            children="Zugriff verweigert – nur für Admins.",
            color="red"
        )

    return dmc.Container([
        dmc.Title("Benutzerverwaltung", order=2, mb="md"),
        dmc.Button("Aktualisieren", id=make_id("refresh"), mb="md"),
        html.Div(id=make_id("table"))
    ], size="md")

# --- Nutzerliste aktualisieren ---
@callback(
    Output(make_id("table"), "children"),
    Input(make_id("refresh"), "n_clicks"),
    prevent_initial_call=True
)
def refresh_users(_=None):
    users = load_users()
    logger.info(f"{len(users)} Benutzer geladen.")

    return [
        dmc.Group([
            dmc.Text(email, w="30%"),
            dmc.Select(
                id={"type": "role-select", "index": user_id},
                data=["admin", "coach", "player"],
                value=role,
                w=150
            ),
            dmc.Button("Löschen", color="red", variant="light", id={"type": "delete-user", "index": user_id})
        ], justify="space-between", mb="xs")
        for user_id, email, role in users
    ]

# --- Rollenänderung speichern ---
@callback(
    Output(make_id("table"), "children", allow_duplicate=True),
    Input({"type": "role-select", "index": ALL}, "value"),
    State({"type": "role-select", "index": ALL}, "id"),
    prevent_initial_call="initial_duplicate"
)
def change_roles(new_roles, ids):
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            for role, id_dict in zip(new_roles, ids):
                user_id = id_dict["index"]
                logger.info(f"Setze Rolle {role} für User {user_id}")
                cur.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
    return refresh_users()

# --- Benutzer löschen ---
@callback(
    Output(make_id("table"), "children", allow_duplicate=True),
    Input({"type": "delete-user", "index": ALL}, "n_clicks"),
    State({"type": "delete-user", "index": ALL}, "id"),
    prevent_initial_call="initial_duplicate"
)
def delete_users(n_clicks_list, ids):
    if not ctx.triggered_id:
        return dash.no_update

    delete_id = ctx.triggered_id["index"]
    logger.info(f"Triggered delete ID: {delete_id}")

    # Validierung: Ist es wirklich eine UUID?
    import uuid
    try:
        delete_id = str(uuid.UUID(delete_id))
    except ValueError:
        logger.error(f"Ungültige UUID: {delete_id}")
        return dmc.Alert(f"Ungültige Benutzer-ID: {delete_id}", color="red")

    try:
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (delete_id,))
        logger.info(f"Benutzer {delete_id} gelöscht.")
        return refresh_users()
    except Exception as e:
        logger.exception("Fehler beim Löschen")
        return dmc.Alert(f"Fehler beim Löschen: {str(e)}", color="red")