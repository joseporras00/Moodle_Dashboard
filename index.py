import base64
import io
import arff
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
import os
from dash.dependencies import Input, Output, State
import dash_auth
from app import app
import pages
from data_reader import *

VALID_USERNAME_PASSWORD_PAIRS = {
    'josepo': 'admin'
}

server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dbc.Container(
    [html.Div(
        [          
            dcc.Location(id="url", refresh=False),
            dbc.Navbar(
                children=[
                    html.A(
                        # Use row and col to control vertical alignment of logo / brand
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Img(
                                        src=app.get_asset_url("logo.png"), height="30px"
                                    )
                                ),
                                dbc.Col(
                                    dbc.NavbarBrand(
                                        "Moodle Dashboard", className="ml-2"
                                    )
                                ),
                            ],                                               
                            className="ml-auto flex-nowrap mt-3 mt-md-0",
                            align="center",
                        ),
                        href=app.get_relative_path("/"),
                    ),
                    dbc.Row(
                        children=[
                            
                            dbc.Col(dbc.NavLink("Upload", href=app.get_relative_path("/upload"))),
                            dbc.Col(dbc.NavLink("Train models", href=app.get_relative_path("/train"))),
                            dbc.Col(dbc.NavLink("Predict", href=app.get_relative_path("/predict"))),
                        ],
                        className="6-columns",
                        style={"paddingLeft": "480px"}
                    ),
                ]
            ),
            dcc.Store(id='stored-data',data=None,storage_type='local'),
            #BODY
            html.Div(id='upload-div',
                children=[
                    dcc.Upload(
                        id="upload-data",
                        children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        # Allow multiple files to be uploaded
                        multiple=False,
                    ),       
                ]),
            html.Div(id="page-content"),
        ]
    ),
    
    ],
)

@app.callback(Output('stored-data','data'),[
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def update_data(contents, filename):
    if contents:
        content_type, content_string = contents.split(",")

        decoded = base64.b64decode(content_string)
        try:
            if "csv" in filename:
               # Assume that the user uploaded a CSV or TXT file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")),header=0)
            elif "xls" in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded),header=0)
            elif "txt" or "tsv" in filename:
               # Assume that the user upl, delimiter = r'\s+'oaded an excel file
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")), delimiter=r"\s+",header=0)
        except Exception as e:
            print(e)
            return html.Div(["There was an error processing this file."])  
        
        return df.to_dict('records')
   
          
@app.callback(Output("page-content", "children"),Output('upload-div', 'hidden'), [Input("url", "pathname")])
def display_page_content(pathname):
        path = app.strip_relative_path(pathname)
        if not path:
            return pages.home.layout(), False
        elif path == "upload":
            return pages.upload.layout(), True
        elif path == "train":
            return pages.models.layout(), True 
        elif path == "predict":
            return pages.predict.layout(), True 
        else:
            return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
