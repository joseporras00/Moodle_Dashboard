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
            dcc.Store(id='stored-predictData',data=None,storage_type='local'),
            dcc.Store(id='predicted_table',data=None,storage_type='local'),
            #BODY
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
            dcc.Checklist(
                ['Does it have header?'],
                ['Does it have header?'],
                id='header',                
            ),
            html.Br(),
            html.H5('Separator'),
            dcc.RadioItems([
                    {'label': 'Comma', 'value': 'comma'},
                    {'label': 'Semicolon', 'value': 'semicolon'},
                    {'label': 'Tabulator', 'value': 'tab'}
                ],
                'comma',
                inline=False,
                id='separator',
            ),
            html.Br(),
            html.Div(id="predict-content"),
            html.Div(id='download-btn',
                     children=[dbc.Button(id='btn',
                        children=[html.I(className="fa fa-download mr-1"), "Download"],
                        color="info",
                        className="mt-1"
                        ),
                    ],
                    hidden=True,
            ),
            dcc.Download(id="download-component"),
            ]
    ),
    ]
    

@app.callback(Output('stored-predictData','data'),[
    Input('upload-predictData', 'contents'),
    Input('upload-predictData', 'filename')]
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
   
          
@app.callback(
    Output("predict-content", "children"),
    Output("predicted_table", "data"),
    Output("download-btn", "hidden"),
    [Input('stored-predictData','data'),],
    prevent_initial_call=True
)
def display(data):
    if data!=None:
        df=pd.DataFrame(data)
        df_1=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2})
        df_2=df_1.iloc[1:,:-1]
        model=joblib.load(open('./assets/my_model.joblib','rb'))
        predictions=model.predict(df_2)
        df_pred = pd.DataFrame (predictions, columns = ['predicted'])
        df_merged = pd.concat([df, df_pred], axis=1, join='inner')
        return [html.H2("Predictions"),
                html.Div(
                    dash_table.DataTable(data=df_merged.to_dict('records'), 
                                            columns=[{"name": i, "id": i} for i in df_merged.columns],
                                            editable=False,
                                            style_table={'overflowX': 'scroll'},
                                            filter_action='native',
                                            sort_action='native',
                                            sort_mode='multi',
                                            column_selectable='single',
                                            selected_columns=[],
                                            selected_rows=[],
                                            page_action='native',
                                            page_current= 0,
                                            page_size= 20,
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
    if data!=None:
        df=pd.DataFrame(data).copy()
        return dcc.send_data_frame(df.to_csv, "predicted_data.csv")
    