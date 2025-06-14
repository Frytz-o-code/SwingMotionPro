# app/pages/admin.py

import dash
from dash import html, Output, Input, State, callback, ctx
import dash_mantine_components as dmc
from dash import MATCH, ALL
from app.db import get_db_connection
from app.auth import get_user_role

dash.register_page(__name__, path="/admin", name="Adminbereich")

# Layout mit Nutzertabelle
def layout():
    if get_user_role() != "admin":
        return dmc.Alert(
            title="Nicht erlaubt",
            children="Zugriff verweigert – nur für Admins.",
            color="red"
        )

    return dmc.Container([
        dmc.Title(children="Benutzerverwaltung", order=2, mb="md"),
        dmc.Button(children="Aktualisieren", id="admin-refresh", mb="md"),
        html.Div(id="user-table")
    ], size="md")

@callback(
    Output("user-table", "children"),
    Input("admin-refresh", "n_clicks"),
    prevent_initial_call=True
)
def refresh_users(n_clicks):
    users = load_users()

    rows = []
    for user in users:
        user_id, email, role = user
        rows.append(
            dmc.Group([
                dmc.Text(children=email, w="30%"),
                dmc.Select(
                    id={"type": "role-select", "index": user_id},
                    data=["admin", "coach", "player"],
                    value=role,
                    w=150
                ),
                dmc.Button(children="Löschen", color="red", variant="light", id={"type": "delete-user", "index": user_id})
            ], justify="space-between", mb="xs")
        )

    return rows

@callback(
    Output("user-table", "children", allow_duplicate=True),
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
                cur.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
    return refresh_users(0)

@callback(
    Output("user-table", "children", allow_duplicate=True),
    Input({"type": "delete-user", "index": ALL}, "n_clicks"),
    State({"type": "delete-user", "index": ALL}, "id"),
    prevent_initial_call="initial_duplicate"
)
def delete_users(n_clicks_list, ids):
    if not ctx.triggered_id:
        return dash.no_update

    delete_id = ctx.triggered_id["index"]
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s", (delete_id,))
    return refresh_users(0)