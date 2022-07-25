import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from utils.helpers import *
from utils.figures import *

from app import *
from data_reader import *
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'
df_prueba=read_data('data/moodle7numericos.csv')

def layout():
    return [
        html.Div(
            children=[
                dbc.Card(
                    children=[
                        dbc.CardHeader("Bienvenido!"),
                        dbc.CardBody(
                            [
                                dcc.Markdown(
                                    """
                                    Esta es una aplicación creada para estudiar los datos de las asignaturas en moodle y así ayudar a los profesores a predecir futuros resultados de sus alumnos. 
                                    Esta aplicación permite crear modelos predictivos y de clasificación para incluir la minería de datos en los nuevos entornos educativos.
                                    El código de esta aplicación está disponible en: https://github.com/joseporras00/Moodle_Dashboard""",
                                    style={"margin": "0 10px"},
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2("DataFrame sin Procesar"),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    dash_table.DataTable(data=df_prueba.to_dict('records'), 
                                         columns=[{"name": i, "id": i} for i in df_prueba.columns],
                                        style_table={'minWidth': '100%'},
                                        filter_action='native',
                                        sort_action='native',
                                        sort_mode='multi',
                                        column_selectable='single',
                                        row_selectable='multi',
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action='native',
                                        page_current= 0,
                                        page_size= 20,
                                    ),title='DataFrame Sin Procesar'
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.Row([html.Div(id='contenido'),]),
            ],                
        )
    ]

@app.callback(
    Output("contenido", "children"),
    [Input("stored-data", "data")],
)
def update_tabla(data):
    df=pd.DataFrame(data)
    return [html.H2("DataFrame Procesado"),
            html.Div(
                dash_table.DataTable(data=df.to_dict('rows'), 
                                         columns=[{"name": i, "id": i} for i in df.columns],
                                         style_table={'minWidth': '100%'},
                                        filter_action='native',
                                        sort_action='native',
                                        sort_mode='multi',
                                        column_selectable='single',
                                        row_selectable='multi',
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action='native',
                                        page_current= 0,
                                        page_size= 20,
                    ),title='DataFrame Sin Procesar',
            ),            
            dbc.Row(
                            [
                            dbc.Col(
                                daq.LEDDisplay(
                                    id='records',
                                    value=str(df.shape[0]),
                                    label = 'Records',
                                    size=FONTSIZE,
                                    color = FONTCOLOR,
                                    backgroundColor=BGCOLOR
                                )
                            ),
                            dbc.Col(
                                daq.LEDDisplay(
                                    id='variables',
                                    value=str(df.shape[1]),
                                    label = 'variables',
                                    size=FONTSIZE,
                                    color = FONTCOLOR,
                                    backgroundColor=BGCOLOR
                                ),
                            ),
                            dbc.Col(
                                daq.LEDDisplay(
                                    id='numeric',
                                    value=str(len([i for i in list(df.columns) if df.dtypes[i] in ['float64','int64']])),
                                    label = 'numeric',
                                    size=FONTSIZE,
                                    color = FONTCOLOR,
                                    backgroundColor=BGCOLOR
                                ),
                            ),
                            dbc.Col(
                                daq.LEDDisplay(
                                    id='categorical',
                                    value=str(len([i for i in list(df.columns) if df.dtypes[i] in ['object']])),
                                    label = 'categorical',
                                    size=FONTSIZE,
                                    color = FONTCOLOR,
                                    backgroundColor=BGCOLOR
                                )
                            ),
                            ]
                        ),
        ]
    
