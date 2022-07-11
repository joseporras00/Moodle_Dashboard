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
                html.H2("DataFrame sin Procesar"),
                html.Div(
                    dash_table.DataTable(data=df_prueba.to_dict('records'), 
                                         columns=[{"name": i, "id": i} for i in df_prueba.columns],
                                         editable=True,
                                        filter_action='native',
                                        sort_action='native',
                                        sort_mode='multi',
                                        column_selectable='single',
                                        row_selectable='multi',
                                        row_deletable=True,
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action='native',
                                        page_current= 0,
                                        page_size= 20,
                    ),title='DataFrame Sin Procesar'
                ),
                html.Div(id='contenido'),                
                #html.Div(id='contadores'),                
                html.Div(id='pie_pass'),
                #dcc.Graph(id='heatmap-graph'),#, figure = create_heatmap(df_moodle_p)),
                #dcc.Graph(id='bar-graph'),#, figure = serve_bar(df_moodle)),
                #dcc.Graph(id='roc-graph'),#, figure = serve_roc_curve(df_moodle_p)),
                #dcc.Graph(id='conf-matrix-graph-svc'),#, figure = serve_pie_confusion_matrix_svc(df_moodle_p)),
                #dcc.Graph(id='conf-matrix-graph-2'),#, figure = serve_pie_confusion_matrix_GB(df_moodle_p)),
                #dcc.Graph(id='conf-matrix-graph-3'),#, figure = serve_pie_confusion_matrix_rf(df_moodle_p)),
                #dcc.Graph(id='conf-matrix-graph-4'),#, figure = serve_pie_confusion_matrix_logr(df_moodle_p)),
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
                                         editable=True,
                                        filter_action='native',
                                        sort_action='native',
                                        sort_mode='multi',
                                        column_selectable='single',
                                        row_selectable='multi',
                                        row_deletable=True,
                                        selected_columns=[],
                                        selected_rows=[],
                                        page_action='native',
                                        page_current= 0,
                                        page_size= 20,
                    ),title='DataFrame Sin Procesar'
            ),            
            dbc.Row(
                            [
                            dbc.Col(
                                daq.LEDDisplay(
                                    id='records',
                                    #label='Default',
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
                                   #label='Default',
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
                                   #label='Default',
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
                                    #label='Default',
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
    Output("pie-pass", "children"),
    [Input("stored-data", "data")],
)
def update_pie(data):
    if(data!=None):
        df=pd.DataFrame(data)
        col_label = "mark"
        col_values = "Count"
        v = df[col_label].value_counts()
        new2 = pd.DataFrame({
            col_label: v.index,
            col_values: v.values
            })

        fig = go.figure = {
                "data": [
                    {
                    "labels":new2['mark'],
                    "values":new2['Count'],
                    "hoverinfo":"label+percent",
                    "hole": .7,
                    "type": "pie",
                    'marker': {'colors': [
                        '#0052cc',  
                        '#3385ff',
                        '#99c2ff',
                        '#0567ff'
                        ]
                        },
                    "showlegend": True
                }],
                "layout": {
                    "title" : dict(text ="Distribución notas",
                            font =dict(
                                size=20,
                                color = 'white')),
                    "paper_bgcolor":"#111111",
                    "showlegend":True,
                    'height':600,
                    'marker': {'colors': [
                                '#0052cc',  
                                '#3385ff',
                                '#99c2ff',
                                '#0567ff'
                                ]
                            },
                    "annotations": [
                        {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "",
                        "x": 0.2,
                        "y": 0.2
                        }
                    ],
                    "showlegend": True,
                    "legend":dict(fontColor="white",tickfont={'color':'white' }),
                    "legenditem": {
                        "textfont": {
                            'color':'white'
                        }
                    }
                } }
        #dcc.Graph(figure=fig),
        return [px.bar(data_frame=df,
                       x=new2['mark'],
                       y=new2['Count'],
                       title='n_q_a by student'
                       ),
                ]
    
"""@app.callback(
    Output("heatmap-graph", "figure"),
    #Output("roc-graph", "figure"),
    #Output("bar-graph", "figure"),
    #Output("conf-matrix-graph-svc", "figure"),
    #Output("conf-matrix-graph-2", "figure"),
    #Output("conf-matrix-graph-3", "figure"),
    #Output("conf-matrix-graph-4", "figure"),
    [Input("stored-data", "data")],
)
def update_graphs(data):
    if(data!=None):
        df=pd.DataFrame(data)
        return create_heatmap(df)#, serve_roc_curve(df), serve_bar(df), serve_pie_confusion_matrix_svc(df), serve_pie_confusion_matrix_rf(df),\
                #serve_pie_confusion_matrix_GB(df), serve_pie_confusion_matrix_logr(df)"""