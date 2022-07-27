import base64
from genericpath import exists
import io
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd
import os
from dash.dependencies import Input, Output, State
from scipy.io.arff import loadarff
import dash_auth
from app import app
import pages
from data_reader import *

VALID_USERNAME_PASSWORD_PAIRS = {
    'josepo': 'admin',
    'cristobal': 'admin'
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
                        dbc.Row(
                            [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url("logo_moodle.png"), height="80px"
                                    )
                                ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "Moodle Dashboard", className="ms-2"
                                )
                            ),
                            ],                                                                     
                            className="g-0 ml-auto flex-nowrap mt-3 mt-md-0",
                            align="center",
                        ),
                        href=app.get_relative_path("/"),
                    ),
                    dbc.Row(
                        [
                        dbc.Collapse(
                            dbc.Nav(
                                [                                    
                                    dbc.NavItem(dbc.NavLink("Home", href=app.get_relative_path("/"))),
                                    dbc.NavItem(dbc.NavLink("Upload", href=app.get_relative_path("/upload"))),
                                    dbc.NavItem(dbc.NavLink("Train models", href=app.get_relative_path("/train"))),
                                    dbc.NavItem(dbc.NavLink("Predict", href=app.get_relative_path("/predict"))),
                                ],
                                className="w-100",
                                fill=True,
                                horizontal='end'
                            ),
                            navbar=True,
                            is_open=True,
                        ),
                        ],
                        className="flex-grow-1",
                    ),  
                ],
                
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
                dbc.Alert(["No se han añadido los datos para realizar las funcionalidades, introducelos para continuar"],
                                id="alert-auto",
                                is_open=False,
                                dismissable=True,
                                fade=True,
                ),
            html.Div(id="page-content"),
        ]
    ),
    
    ]
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
   
          
@app.callback(Output("page-content", "children"),Output('upload-div', 'hidden'),Output("alert-auto", "is_open"), [Input("url", "pathname"),Input('stored-data','data')],
              prevent_initial_call=True
)
def display_page_content(pathname,data):
        path = app.strip_relative_path(pathname)
        if data!=None:
            if not path:
                return pages.home.layout(), False, False
            elif path == "upload":
                return pages.upload.layout(), True, False
            elif path == "train":
                return pages.models.layout(), True , False
            elif path == "predict":
                return pages.predict.layout(), True, False
            else:
                return "404"
        else:
            path=app.get_relative_path("/")
            return pages.home.layout(), False, True


if __name__ == "__main__":
    app.run_server(debug=True)
