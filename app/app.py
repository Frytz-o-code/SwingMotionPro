
# app/app.py

import os
import dash
from dash import callback, Output, Input, State, html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import session
from app.auth import logout_user
from app.utils.session_helpers import is_logged_in, current_user_role, current_user_email

# Dash-Initialisierung
app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=dmc.styles.ALL,
    suppress_callback_exceptions=True
)
app.title = "SwingMotionPro"

server = app.server

# ---------- Navigation ----------

def create_nav_link(icon, label, href):
    return dmc.NavLink(
        label=label,
        href=href,
        active="exact",
        leftSection=DashIconify(icon=icon)
    )

def get_user_nav_links():
    links = []

    if current_user_role() == "admin":
        links.append(create_nav_link("carbon:user-admin", "Admin", "/admin"))

    if is_logged_in():
        links.append(dmc.Anchor("Logout", href="/logout", color="red"))
        links.append(dmc.Text(f"Angemeldet als: {current_user_email()}", size="xs", c="dimmed"))
    else:
        links.append(dmc.Anchor("Login", href="/login", color="blue"))

    return dmc.Stack(links, gap="xs", mt="lg")

navbar_links = dmc.Box(
    [
        create_nav_link("radix-icons:rocket", "Home", "/"),
        dmc.Divider(label="Golf", style={"marginTop": 20, "marginBottom": 10}),
        dmc.Stack(
            [
                create_nav_link(page["icon"], page["name"], page["path"])
                for page in dash.page_registry.values()
                if page["path"].startswith("/golf")
            ]
        ),
        dmc.Divider(label="Benutzer", style={"marginTop": 20}),
        get_user_nav_links()
    ]
)

# ---------- AppShell ----------

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            dmc.Group(
                [
                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                    dmc.Title("SwingMotionPro", order=2),
                ],
                h="100%",
                px="md",
                align="center",
                gap="md"
            )
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=navbar_links,
            p="md",
        ),
        dmc.AppShellMain([
            dash.page_container,
            dmc.Center(
                "© 2025 SwingMotionPro", 
                style={"padding": "1rem", "fontSize": 12, "color": "#999"}
            )
        ])
    ],
    header={"height": 60},
    navbar={"width": 280, "breakpoint": "sm", "collapsed": {"mobile": True}},
    padding="md",
    id="appshell"
)

app.layout = dmc.MantineProvider(
    children=layout,
    theme={"colorScheme": "light"},  # optional
)

# ---------- Burger Callback ----------

@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def navbar_is_open(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar
# ---------- Run the app ---------- 
# app/app.py
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
# For production, use a WSGI server like Gunicorn:
# gunicorn app:server --bind        
