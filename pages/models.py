import pandas as pd
import numpy as np
import datetime as dt
import base64
import io
import os
import base64
import seaborn as sn
import matplotlib as plt
import pandas as pd
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from data_reader import *
from utils.modeling import *
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash import callback_context
from app import app

server = app.server


models = ['LGBM', 'Random Forest','SVC', 'KNN', 'GNB', 'DT','MLP', 'ADABoost','Logistic']
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'

def layout():
    return[
            dcc.Store(id='stored-model',data=None,storage_type='local'),
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

            html.P('Selecciona el Target', className='control_label'),
            dcc.Dropdown(
                id='select_target',
                multi=False,
                value='mark',
                options=['mark'],
                clearable=False,
                className='dcc_control',
            ),
            html.P('Selecciona las variables independientes', className='control_label'),
            dcc.Dropdown(
                id='select_independent',
                multi=True,
                options=['course','n_assignment','n_posts','n_read','n_quiz','n_quiz_a','n_quiz_s','total_time_assignment','total_time_quiz','total_time_forum'],
                value=['course','n_assignment','n_posts','n_read','n_quiz','n_quiz_a','n_quiz_s','total_time_assignment','total_time_quiz','total_time_forum'],
                className='dcc_control',
            ),
            html.P('Selecciona numero de Splits', className='control_label'),
            daq.NumericInput(
                id='id-splits',
                min=0,
                max=10,
                size = 75,
                value=2
            ),  
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
            html.H5('Comenzar el modelado'),
            daq.PowerButton(
                id = 'id-daq-switch-model',
                on='False',
                color='#1ABC9C', 
                size = 75,
                label='Comenzar'
            ),
#--------------------------------------------------------------------------------------------------------------------
            html.Br(),
            dbc.Row(
                [
                dbc.Col(
                    daq.LEDDisplay(
                        id='precision',
                        #label='Default',
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
                        #label='Default',
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
                        #label='Default',
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
                        #label='Default',
                        value= 0,
                        label = 'F1',
                        size=FONTSIZE,
                        color = FONTCOLOR,
                        backgroundColor=BGCOLOR
                    ),
                    ]
                )
                ]
            ), 
            html.Br(),
            html.Button('Export model', id='exp_button', n_clicks=0),
            html.Div(id='container-button-timestamp'),
            html.Br(),
#--------------------------------------------------------------------------------------------
            html.H5('Precission'),
            html.Div(
                [dcc.Graph(id='main_graph')],
                className='pretty_container six columns',
            ),
            html.Br(),
            html.H5('Confussion Matrix'),
            html.Div(
                [dcc.Graph(id='conf_matrix')],
                className='pretty_container six columns',
            ),
            html.Br(),
            dbc.CardHeader("Report"),
                        dbc.CardBody(
                            [
                                html.Pre(id='report-div',   
                                )
                            ]
                        ),
            #html.H5('Roc curve'),
            #html.Div(
            #    [dcc.Graph(id='roc_curve')],
            #    className='pretty_container six columns',
            #),
            #html.H5('Pie Confussion Matrix'),
            #html.Div(
            #    [dcc.Graph(id='pie_conf_matrix')],
            #    className='pretty_container six columns',
            #),
            
    ]
    
    
@app.callback(
    [
        Output('precision', 'value'),
        Output('recall', 'value'),
        Output('accuracy', 'value'),
        Output('f1', 'value'),
        Output('id-daq-switch-model', 'on'),
        Output('main_graph', 'figure'),
        Output('conf_matrix', 'figure'), 
        Output('report-div', 'children'), 
   ],
   [
       Input('stored-data', 'data'),
       Input('select_target', 'value'),
       Input('select_independent', 'value'),
       Input('slider', 'value'),
       Input('id-splits', 'value'),
       Input('select_models', 'value')        
   ]
)
def measurePerformance(data, target, independent, slider,splits, selected_models):
    df=pd.DataFrame(data)
    precision, recall, accuracy, f1, fig1, fig2, reporte  = buildModel(df,target,independent, slider,splits, selected_models)

    return precision, recall, accuracy,f1,True, fig1,fig2, reporte

@app.callback(
    [
        Output('container-button-timestamp', 'children'),
   ],
   [
       Input('exp_button', ', n_clicks'),
   ]
)
def export_model(n):
    msg = 'Aun no se ha exportado un modelo'
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'exp_button' in changed_id:
        msg = 'Modelo exportado'
        exportar_modelo()
    return [html.Div(msg)]
