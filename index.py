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

# A dictionary that contains the username and password for the authentication.
VALID_USERNAME_PASSWORD_PAIRS = {
    'josepo': 'admin',
    'cristobal': 'admin'
}

# The way to run the app in a local server.
server = app.server

# The way to authenticate the user.
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = dbc.Container(
    [html.Div(
        [          
            # A component that allows to get the current URL of the page.
            dcc.Location(id="url", refresh=False),
            # Creating the navbar of the app.
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
                    # Creating the items of the navbar.
                    dbc.Row(
                        [
                        dbc.Collapse(
                            dbc.Nav(
                                [                                    
                                    dbc.NavItem(dbc.NavLink("Home", href=app.get_relative_path("/"))),
                                    dbc.NavItem(dbc.NavLink("Dashboard", href=app.get_relative_path("/dash"))),
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
            # A component that allows to store data in the whole the app.
            dcc.Store(id='stored-data',data=None,storage_type='session'),
            dcc.Store(id='stored-data2',data=None,storage_type='session'),
            #BODY
            # A component that allows to upload a file.
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
                dbc.Alert(["The data to perform the funcionalities has not been added, upload them to continue"],
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

@app.callback(Output('stored-data2','data'),[
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')]
)
def update_data(contents, filename):
    """
    It takes the contents of the uploaded file and converts it to a pandas dataframe. 
    
    The dataframe is then converted to a dictionary to be returned. 
    
    The dictionary is then used to update the data in the table.
    
    :param contents: the contents of the uploaded file
    :param filename: The name of the uploaded file
    :return: A list of dictionaries.
    """
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
        """
        If the path is empty, return the home page. If the path is "dash", return the dashboard page. If the
        path is "train", return the models page. If the path is "predict", return the predict page.
        Otherwise, return a 404 page
        
        :param pathname: The pathname argument is the current location of the page
        :param data: The dataframe that is uploaded by the user
        :return: a list of dash components.
        """
        path = app.strip_relative_path(pathname)
        if not path:
            if data!=None:
                return pages.home2.layout(), False, False
            else:
                return pages.home2.layout(), False, True
        elif path == "dash":
            if data!=None:
                return pages.dashboard.layout(), True, False
            else:
                return [dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("ERROR"),close_button=False),
                                dbc.ModalBody([html.I(className="bi bi-exclamation-circle fa-2x"),"  No data uploaded"]),
                                dbc.ModalFooter(dbc.Button([dcc.Link('Go back to home', href='/',style={'color': 'white'}),])),
                            ],
                            id="modal-fs",
                            is_open=True,
                            keyboard=False,
                            backdrop="static",
                        ),], False, False
        elif path == "train":
            if data!=None:
                return pages.models.layout(), True , False
            else:
                return [dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("ERROR"),close_button=False),
                                dbc.ModalBody([html.I(className="bi bi-exclamation-circle fa-2x"),"  No data uploaded"]),
                                dbc.ModalFooter(dbc.Button([dcc.Link('Go back to home', href='/',style={'color': 'white'}),])),
                            ],
                            id="modal-fs",
                            is_open=True,
                            keyboard=False,
                            backdrop="static",
                        ),], False, False
        elif path == "predict":
            if os.path.exists('assets/my_model.joblib')==True:
                return pages.predict.layout(), True, False
            else:
                return [dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("ERROR"),close_button=False),
                                dbc.ModalBody([html.I(className="bi bi-exclamation-circle fa-2x"),"  No model on the server to make predictions..",
                                               " Upload a data file to create and train a model."]),
                                dbc.ModalFooter(dbc.Button([dcc.Link('Go back to home', href='/',style={'color': 'white'}),])),
                            ],
                            id="modal-fs",
                            is_open=True,
                            keyboard=False,
                            backdrop="static",
                        ),], False, False
        else:
            return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
