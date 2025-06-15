# app/app.py
from app.logging_config import setup_logging
setup_logging()
import os
import dash
from dash import callback, Output, Input, State, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session

from app.utils.session_helpers import is_logged_in, current_user_role, current_user_email
from app.auth import logout_user


import logging
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
        dmc.Divider(label="Golf", style={"marginTop": 20, "marginBottom": 10}),
    ]

    # Dynamisch: alle Golf-Seiten
    golf_pages = [
        create_nav_link(page["icon"], page["name"], page["path"])
        for page in dash.page_registry.values()
        if page["path"].startswith("/golf")
    ]
    links.extend(golf_pages)

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
    children=dmc.AppShell(
        id="appshell",
        padding="md",
        withBorder=True,
        children=[
            dmc.AppShellHeader(
                dmc.Group(
                    [
                        dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                        dmc.Title("SwingMotionPro", order=2),
                    ],
                    h="100%", px="md", align="center", gap="md"
                )
            ),
            dmc.AppShellNavbar(
                id="navbar",
                children=create_navbar(),
                p="md"
            ),
            dmc.AppShellMain(
                [
                    dash.page_container,
                    dmc.Center("© 2025 SwingMotionPro", style={"padding": "1rem", "fontSize": 12, "color": "#999"})
                ]
            )
        ]
    )
)

app.layout = create_app_layout  # wichtig: keine Klammern!

# --- Burger Callback ---
@callback(
    Output("burger", "opened"),
    Input("burger", "opened"),
    prevent_initial_call=True
)
def toggle_navbar(opened):
    return not opened

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