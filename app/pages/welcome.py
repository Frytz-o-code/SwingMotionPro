# pages/welcome.py

import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(__name__, path="/", name="Welcome")

def layout():
    return dmc.Center(
        dmc.Paper(
            [
                dmc.Title("Welcome to SwingMotionPro!", order=1, ta="center"),
                dmc.Text(
                    "Get started by using the navigation on the left.",
                    ta="center",
                    mt="md",
                    size="lg"
                ),
                dmc.Divider(mb="md", mt="md"),
                dmc.Text("Enjoy your analysis!", ta="center", c="dimmed"),
            ],
            p="xl",
            shadow="md",
            radius="md",
            withBorder=True,
            style={"maxWidth": 500, "margin": "auto"}
        ),
        style={"height": "80vh"}
    )