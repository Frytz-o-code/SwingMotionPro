import dash
from dash import html
import flask

app = dash.Dash(__name__)
server = app.server  # wichtig für gunicorn

app.layout = html.Div("Hello Fly.io!")