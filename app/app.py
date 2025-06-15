import os
import dash
from dash import callback, Output, Input, State, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session
import logging

from app.logging_config import setup_logging
from app.utils.session_helpers import is_logged_in, current_user_role, current_user_email
from app.auth import logout_user

setup_logging()
logger = logging.getLogger("app")
logger.info("SwingMotionPro wird gestartet...")

# --- Dash App Initialisierung ---
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=dmc.styles.ALL,
    suppress_callback_exceptions=True,
)

app.server.secret_key = os.getenv("SECRET_KEY", "dev-secret")
app.title = "SwingMotionPro"
server = app.server

# --- Navigation ---
def create_nav_link(icon, label, href):
    return dmc.NavLink(
        label=label,
        href=href,
        active="exact",
        leftSection=DashIconify(icon=icon)
    )

def create_navbar():
    links = [
        create_nav_link("radix-icons:rocket", "Home", "/"),
        dmc.Divider(label="Seiten", style={"marginTop": 20, "marginBottom": 10}),
    ]

    # Alle registrierten Seiten außer Login/Logout/Admin
    visible_pages = [
        page for page in dash.page_registry.values()
        if page["path"] not in ["/login", "/logout", "/admin"]
    ]

    # Sortiere optional alphabetisch oder nach Wunsch
    visible_pages.sort(key=lambda p: p["name"])

    # Einträge erstellen
    for page in visible_pages:
        links.append(create_nav_link(page.get("icon", "mdi:golf"), page["name"], page["path"]))

    links.append(dmc.Divider(label="Benutzer", style={"marginTop": 20}))

    if is_logged_in():
        if current_user_role() == "admin":
            links.append(create_nav_link("carbon:user-admin", "Admin", "/admin"))
        links.append(dmc.Anchor("Logout", href="/logout", c="red"))
        links.append(dmc.Text(f"Angemeldet als: {current_user_email()}", size="xs", c="dimmed"))
    else:
        links.append(dmc.Anchor("Login", href="/login", c="blue"))

    return dmc.Stack(links, gap="xs", mt="lg")
# --- Layout --- 

def create_app_layout():
    return dmc.MantineProvider(
        theme={"colorScheme": "light"},
        children=[
            dmc.AppShell(
                id="appshell",
                padding="md",
                withBorder=True,
                children=[
                    # Header mit Burger
                    dmc.AppShellHeader(
                        dmc.Group(
                            [
                                dmc.Burger(id="burger", size="sm", opened=False, hiddenFrom="sm"),
                                dmc.Title("SwingMotionPro", order=2),
                            ],
                            h="100%", px="md", align="center", gap="md"
                        )
                    ),

                    # Flexbox Layout: Sidebar + Main
                    html.Div(
                        id="navbar",
                        children=[
                            dmc.Text("NAVBAR DEBUG VISIBLE", c="red", fw=700),
                            create_navbar()
                        ],
                        style={
                            "display": "block",  # <<< fix: sichtbar beim Start
                            "width": "250px",
                            "padding": "1rem",
                            "backgroundColor": "#f8f9fa",
                            "borderRight": "1px solid #ccc",
                            "flexShrink": 0
                        }
                    ),
                    html.Div(
                        children=[
                            dash.page_container,
                            dmc.Center("© 2025 SwingMotionPro", style={"padding": "1rem", "fontSize": 12, "color": "#999"})
                        ],
                        style={"flexGrow": 1, "paddingLeft": "2rem"}
                    )
                ],
                style={"display": "flex", "flexDirection": "row"}
            )
        ]
    )

app.layout = create_app_layout  # ohne Klammern!

# --- Burger Callback: Sidebar anzeigen/ausblenden ---
# Callback – bleibt gleich
@callback(
    Output("navbar", "style"),
    Input("burger", "n_clicks"),
    State("navbar", "style"),
    prevent_initial_call=True
)
def toggle_navbar(n_clicks, current_style):
    current = current_style.get("display", "none") if current_style else "none"
    base = {
        "width": "250px",
        "padding": "1rem",
        "backgroundColor": "#f8f9fa",
        "borderRight": "1px solid #ccc",
        "flexShrink": 0
    }
    return {**base, "display": "none"} if current == "block" else {**base, "display": "block"}


# --- App-Start ---
if __name__ == "__main__":
    app.run(
        debug=True,
        port=8050,
        dev_tools_ui=True,
        dev_tools_props_check=True,
        dev_tools_serve_dev_bundles=True,
        dev_tools_hot_reload=True,
        dev_tools_prune_errors=False,
    )