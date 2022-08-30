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

# Setting the font size, color, and background color for the LED displays.
FONTSIZE = 20
FONTCOLOR = '#F5FFFA'
BGCOLOR ='#3445DB'

def layout():
    return [
        html.Div(
            children=[
                dbc.Card(
                    children=[
                        # A card with information about the web aplication.
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
                dbc.Spinner(dbc.Row(
                    [
                        dbc.Col(
                            [
                                # Creating a table with the data.
                                html.Div(id="Unp-table", children=[html.H3("Data"),html.Br(),
                                            dash_table.DataTable(
                                                # Making the table scrollable.
                                                style_table={'overflowX': 'scroll'},
                                                # Allows the user to filter the data in the table.
                                                filter_action='native',sort_action='native',
                                                # Allows the user to sort the data in the table.
                                                sort_mode='multi',
                                                # Preventing the user from deleting rows.
                                                row_deletable=False,
                                                # It allows the user to select a single column.
                                                column_selectable='single',
                                                selected_columns=[],
                                                selected_rows=[],
                                                page_action='native',
                                                page_current= 0,
                                                # Setting the table to have 20 rows per page
                                                page_size= 20,
                                                # To have a different background color for odd rows.
                                                style_data_conditional=[        
                                                    {'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'}
                                                ],
                                                id="datatable-data"
                                                ),
                                                html.Br(),
                                                
                                                # Creating a button that will trigger the callback to discretize the data.
                                                html.Div([
                                                        html.Button('Discretize', id='btn', n_clicks=0),
                                                        ],
                                                        style={'verticalAlign': 'middle', 'display': 'inline'},
                                                        className='text-center',
                                                ),
                                                html.Br(),html.Br(),
                                ],hidden=True),
                            ]
                        ),
                    ]
                )),
                dbc.Spinner(dbc.Row(
                    [
                        dbc.Col(
                            [
                               html.Div(id="leds"),
                            ]
                        ),
                    ]
                )),
            ],                
        )
    ]

@app.callback(
    Output("datatable-data", "data"),
    Output("datatable-data", "columns"),
    Output("Unp-table", "hidden"),
    [Input("stored-data2", "data"),
     Input("stored-data", "data")],
)
def update_table(data,data2):
    """
    The function returns de data of the table and show it
    
    :param data: the dataframe that is being displayed in the table
    :param data2: This is the dataframe that is being updated
    :return: The dataframe is being returned as a dictionary of rows.
    """
    if data!=None:
        if data2!=None:
            df=pd.DataFrame(data2).copy()
            return df.to_dict('rows'),[{"name": i, "id": i} for i in df.columns],False
        else:
            df=pd.DataFrame(data).copy()
            return df.to_dict('rows'),[{"name": i, "id": i} for i in df.columns],False

@app.callback(
    Output("leds", "children"),
    [Input("datatable-data", "data"),],
    prevent_initial_call=True
)
def update_data(data):
    """
    If the data is not None, then create a dataframe from the data, and return a row of LED displays
    with the number of records, variables, numeric variables, and categorical variables
    
    :param data: the dataframe
    :return: A list of dbc.Row objects.
    """
    if data!=None:
        df=pd.DataFrame(data).copy()
        return [dbc.Row(
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
        
@app.callback(    
    Output("stored-data", "data"),
    [Input("btn", "n_clicks"),],
    State("stored-data2", "data"),
    prevent_initial_call=True
)
def update_data(btn,data):
    """
    If the data is not None and the button has been clicked, then preprocess the data and return it.
    
    :param btn: the button that triggers the callback
    :param data: the dataframe that is stored in the hidden div
    :return: The dataframe is being returned as a dictionary.
    """
    if data!=None and btn>0:
            df=pd.DataFrame(data).copy()
            df2=preprocess_data(df)
            return df2.to_dict('records')                               