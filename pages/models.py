import pandas as pd
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from data_reader import *
from utils.modeling import *
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import callback_context
import json
from utils import modeling

from app import app
import pages

server = app.server


models = ['LGBM', 'Random Forest','SVC', 'KNN', 'GNB', 'DT','MLP', 'ADABoost','Logistic']
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'

def layout():
    return[
            html.Div(id='slider-output-container'),
            html.Br(),
            daq.Slider(
                id = 'slider',
                min=0,
                max=100,
                value=30,
                handleLabel={'showCurrentValue': True,'label': 'SPLIT'},
                step=10,
            ),
            html.Br(),
            html.P('Selecciona el Target', className='control_label'),
            dcc.Dropdown(
                id='select_target',
                multi=False,
                value='mark',
                options=['mark'],
                clearable=False,
                className='dcc_control',
            ),
            html.Br(),
            html.P('Selecciona las variables independientes', className='control_label'),
            dcc.Dropdown(
                id='select_independent',
                multi=True,
                options=['course','n_assignment','n_posts','n_read','n_quiz','n_quiz_a','n_quiz_s','total_time_assignment','total_time_quiz','total_time_forum'],
                value=['course','n_assignment','n_posts','n_read','n_quiz','n_quiz_a','n_quiz_s','total_time_assignment','total_time_quiz','total_time_forum'],
                className='dcc_control',
            ),
            html.Br(),
            html.P('Selecciona numero de Splits', className='control_label'),
            daq.NumericInput(
                id='id-splits',
                min=0,
                max=10,
                size = 75,
                value=2
            ),
            html.Br(),
            html.P('Elige un modelo', className='control_label'),
            dcc.Dropdown(
                id='select_models',
                options = [{'label':x, 'value':x} for x in models],
                value = 'DT',
                multi=False,
                clearable=False,
                className='dcc_control',
            ),
            html.Br(),
            html.Div([
                html.Button('Train', id='btn-train', n_clicks=0),
                ],
                style={'verticalAlign': 'middle', 'display': 'inline'},
                className='text-center',
            ),
            html.Br(),
#--------------------------------------------------------------------------------------------------------------------
            html.Br(),
            dbc.Spinner(dbc.Row(
                [
                dbc.Col(
                    daq.LEDDisplay(
                        id='precision',
                        value=0,
                        label = 'Precision',
                        size=FONTSIZE,
                        color = FONTCOLOR,
                        backgroundColor=BGCOLOR
                    )
                ),
                dbc.Col(
                    daq.LEDDisplay(
                        id='recall',
                        value=0,
                        label = 'Recall',
                        size=FONTSIZE,
                        color = FONTCOLOR,
                        backgroundColor=BGCOLOR
                    ),
                ),
                dbc.Col(
                    [
                    daq.LEDDisplay(
                        id='accuracy',
                        value=0,
                        label = 'Accuracy',
                        size=FONTSIZE,
                        color = FONTCOLOR,
                        backgroundColor=BGCOLOR
                    ), 
                    ]
                ),  
                dbc.Col(
                    [
                    daq.LEDDisplay(
                        id='f1',
                        value= 0,
                        label = 'F1',
                        size=FONTSIZE,
                        color = FONTCOLOR,
                        backgroundColor=BGCOLOR
                    ),
                    ]
                )
                ]
            )),
            html.Br(),
#--------------------------------------------------------------------------------------------
            html.H5('Precission'),
            dbc.Spinner(html.Div(
                [dcc.Graph(id='main_graph')],
                id='div-prec',
                className='pretty_container six columns',
                hidden=True,
            )),
            html.Br(),
            html.H5('Confussion Matrix'),
            dbc.Spinner(html.Div(
                [dcc.Graph(id='conf_matrix')],
                id='div-confm',
                className='pretty_container six columns',
                hidden=True,
            )),
            html.Br(),
            dbc.Spinner([dbc.CardHeader("Report"),
                dbc.CardBody(
                    [
                        html.Pre(id='report-div',)
                    ]
                )]),            
    ]
    
    
@app.callback(
    [
        Output('precision', 'value'),
        Output('recall', 'value'),
        Output('accuracy', 'value'),
        Output('f1', 'value'),
        Output('main_graph', 'figure'),
        Output('conf_matrix', 'figure'), 
        Output('report-div', 'children'),
        Output('div-prec', 'hidden'),
        Output('div-confm', 'hidden'),
   ],
   [
       State('stored-data', 'data'),
       State('select_target', 'value'),
       State('select_independent', 'value'),
       State('slider', 'value'),
       State('id-splits', 'value'),
       State('select_models', 'value'),
       Input('btn-train', 'n_clicks'),      
   ],
   prevent_initial_call=True
)
def measurePerformance(data, target, independent, slider,splits, selected_models, clicks):
    if data!=None:
        df=pd.DataFrame(data).copy()
        precision, recall, accuracy, f1, fig1, fig2, reporte  = buildModel(df,target,independent, slider,splits, selected_models)

        return precision, recall, accuracy,f1, fig1,fig2, reporte, False, False



