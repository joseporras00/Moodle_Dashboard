import base64
import io
import joblib
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from scipy.io.arff import loadarff
from app import app
from data_reader import *
import dash_table
from app import app
import pages
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'


def layout():
    return [html.Div(
        [          
            # Store data in the browser.
            dcc.Store(id='stored-predictData',data=None,storage_type='local'),
            dcc.Store(id='predicted_table',data=None,storage_type='local'),
            # A div that contains the upload component for the data to be predicted.
            html.Div(id='upload-data',
                children=[
                    dcc.Upload(
                        id="upload-predictData",
                        children=html.Div(["Drag and Drop or ", html.A("Select Files")," to prediction"]),
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
            html.Br(),
            html.Br(),
            dbc.Spinner(html.Div(id="predict-content")),
            # A button that is hidden until the user uploads a file. It allows the user to download the predictions.
            html.Div(id='download-btn',
                     children=[dbc.Button(id='btn',
                        children=[html.I(className="fa fa-download mr-1"), "Download"],
                        color="#FB9C34",
                        className="mt-1"
                        ),
                    ],
                    hidden=True,
            ),
            # A component that allows the user to download the data.
            dcc.Download(id="download-component"),
            ]
    ),
    ]
    

@app.callback(Output('stored-predictData','data'),[
    Input('upload-predictData', 'contents'),
    Input('upload-predictData', 'filename')]
)
def update_data(contents, filename):
    """
    If the user uploads a file, the function will read the file and return a dictionary
    of the data. 
    
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
            return None  
        
        return df.to_dict('records')
   
          
@app.callback(
    Output("predict-content", "children"),
    Output("predicted_table", "data"),
    Output("download-btn", "hidden"),
    [Input('stored-predictData','data'),],
    prevent_initial_call=True
)
def display(data):
    """
    It takes the data from the user, loads the model, makes predictions, and returns the predictions in
    a table
    
    :param data: the dataframe to be displayed
    :return: a list of html elements, a dataframe and a boolean value.
    """
    if data!=None:
        df=pd.DataFrame(data)
        df_1=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2})
        df_2=df_1.copy()
        
        # It loads the model from the server.
        model=joblib.load(open('./assets/my_model.joblib','rb'))
        
        # Loading the model.
        f_names=model.feature_names
        # Making predictions.
        predictions=model.predict(df_2[f_names])
        # Merging the predictions with the original data.
        df_pred = pd.DataFrame (predictions, columns = ['predicted'])
        df_merged = pd.concat([df, df_pred], axis=1, join='inner')
        return [html.H2("Predictions"),
                html.Div(
                    dash_table.DataTable(data=df_merged.to_dict('records'), 
                                            columns=[{"name": i, "id": i} for i in df_merged.columns],
                                            # Making the table not editable.
                                            editable=False,
                                            # Making the table scrollable.
                                            style_table={'overflowX': 'scroll'},
                                            # It allows the user to filter the data.
                                            filter_action='native',
                                            # It allows the user to sort the data by multiple columns.
                                            sort_action='native',
                                            sort_mode='multi',
                                            column_selectable='single',
                                            selected_columns=[],
                                            selected_rows=[],
                                            # t allows the user to navigate through the pages of the table.
                                            page_action='native',
                                            page_current= 0,
                                            # The number of rows that will be displayed in the table.
                                            page_size= 20,
                                            # Changing the background color of the odd rows.
                                            style_data_conditional=[        
                                                {'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'}
                                            ],
                        ),
                ),            
                
            ],df_merged.to_dict('records'),False

@app.callback(
    Output("download-component", "data"),
    Input("btn", "n_clicks"),
    State("predicted_table", "data"),
    prevent_initial_call=True,
)
def func(n_clicks,data):
    """
    It takes the data from the table and converts it to a downloadable csv file
    
    :param n_clicks: To perform the callback
    :param data: the dataframe you want to download
    :return: The dataframe is being returned as a csv file.
    """
    if data!=None:
        df=pd.DataFrame(data).copy()
        return dcc.send_data_frame(df.to_csv, "predicted_data.csv")
    