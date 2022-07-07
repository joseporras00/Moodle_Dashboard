import dash
import dash_bootstrap_components as dbc
from urllib.request import urlopen

app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.title = "Moodle Dashboard"
