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
# Reading the data from the csv file and storing it in a dataframe.
df_prueba=read_data('data/moodle7numericos.csv')

def layout():
    return [
        html.Div(
            children=[
                dbc.Card(
                    children=[
                        # A card with a header and a body.
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
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("Unprocessed DataFrame"),
                            ]
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                # Creating a table with the data from the dataframe.
                                html.Div(
                                    dash_table.DataTable(data=df_prueba.to_dict('records'), 
                                         columns=[{"name": i, "id": i} for i in df_prueba.columns],
                                        style_table={'overflowX': 'scroll'},
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
                                        style_data_conditional=[        
                                            {'if': {'row_index': 'odd'},
                                            'backgroundColor': 'rgb(248, 248, 248)'}
                                        ],
                                    ),title='Unprocessed DataFrame'
                                ),
                            ]
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row([html.Div(id='contenido'),]),
            ],                
        )
    ]

@app.callback(
    Output("contenido", "children"),
    [Input("stored-data", "data")],
)
def update_tabla(data):
    """
    It takes the data from the hidden div, and creates a dataframe from it. 
    Then it creates a table from the dataframe, and displays it. 
    Then it creates a row of LED displays, and displays them.
    
    :param data: The data to be displayed in the table.
    :return: A list of html elements.
    """
    df=pd.DataFrame(data).copy()
    return [html.H3("Processed Dataframe"),
                html.Div(
                    dash_table.DataTable(data=df.to_dict('rows'), 
                                            columns=[{"name": i, "id": i, "deletable": True, 'renamable': True} for i in df.columns],
                                            style_table={'overflowX': 'scroll'},
                                            filter_action='native',
                                            sort_action='native',
                                            sort_mode='multi',
                                            row_deletable=True,
                                            row_selectable='single',
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
                        ),title='DataFrame Procesado',
                ),    
                html.Br(),        
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

        
