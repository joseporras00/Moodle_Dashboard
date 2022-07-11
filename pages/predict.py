import base64
import io
import joblib
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
from app import app
from data_reader import *
from app import app
import pages
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'


def layout():
    return [html.Div(
        [          
            dcc.Store(id='predict-model',data=None,storage_type='local'),
            dcc.Store(id='predict-data',data=None,storage_type='local'),
            #BODY
            html.Div(id='model',
                children=[
                    dcc.Upload(
                        id="upload-model",
                        children=html.Div(["Drag and Drop or ", html.A("Select Files")," of selected model"]),
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
            html.Button('Start prediction', id='button', n_clicks=0),
            html.Div(id="predict-content"),
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
    [Input("button", "n_clicks")],
    State('upload-model','data'),
    State('upload-predictData','data'),  
)
def display(btn,model,data):
    if data!=None and model!=None:
        df=pd.DataFrame(data)
        df=df.loc[:-1]
        model=joblib.load(open(model,'rb'))
        predictions=model.predict(df)[0]
        #df.merge(predictions)
        return [html.H2(predictions),
                #html.H2("Predictions"),
                #html.Div(
                #    dash_table.DataTable(data=predictions.to_dict('rows'), 
                #                            columns=[{"name": i, "id": i} for i in df.columns],
                #                            editable=True,
                #                            filter_action='native',
                #                            sort_action='native',
                #                            sort_mode='multi',
                #                            column_selectable='single',
                #                            row_selectable='multi',
                #                            row_deletable=True,
                #                            selected_columns=[],
                #                            selected_rows=[],
                #                            page_action='native',
                #                            page_current= 0,
                #                            page_size= 20,
                #        ),
                #),            
                
            ]

