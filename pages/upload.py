from matplotlib.pyplot import figure
import plotly.graph_objs as go
from data_reader import *

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from app import app
from data_reader import *
from utils.helpers import *
from utils.figures import *
import pages


import pandas as pd
import plotly.express as px

df_main=pd.DataFrame()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}

def makepie(labels,values,texto):
    fig= go.figure = {
            "data": [
                {
                "labels":labels,
                "values":values,
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
                "title" : dict(text =texto,
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
    return fig
    

def layout():
    return [
        html.Div(
            [   
                html.Div(id="output-data-upload"),
                html.Div([
                    html.H5('Elige el curso deseado'),
                    dcc.Dropdown(id='course-dropdown',
                        multi=False,
                        clearable=True,
                        value=None,
                    ),     
                       
                    dcc.Graph(id="Mygraph"),
                ]),              
                
                #dcc.Graph(id='piechart'),
                html.H5('Elige una variable'),
                dcc.Dropdown(id='variable-dropdown',
                    multi=False,
                    clearable=False,
                    options=['n_assignment','n_posts','n_read','n_quiz','n_quiz_a','n_quiz_s','total_time_assignment','total_time_quiz','total_time_forum'],
                    value="n_posts",
                ), 
                html.Div([
                    html.H5("Bar Chart:"),
                    dcc.Graph(id="barchart"),
                ],className='row'),
                
                html.Div([
                    html.H5("Scatter Matrix:"),
                    dcc.Graph(id='matrix'),
                ],className='row'),
                
                html.Div([
                    html.H5("Correlation Matrix:"),
                    dcc.Graph(id='matrix2'),
                ],className='row'),
                
                html.Div([
                    html.H5("Features:"),
                    dcc.Graph(id='feature_graph'),
                ],className='row'),
                     
            ]
        )
    ]
        
        
@app.callback(Output('Mygraph', 'figure'),
    [
    Input('stored-data', 'data'),
    Input('course-dropdown', 'value'),
])
def update_graph(data,curso):
    df = pd.DataFrame(data)
    col_label = "mark"
    col_values = "Count"
    if(curso !=None):
        df = df[df['course'].isin([curso])]
        v=df[col_label].value_counts()
        new2 = pd.DataFrame({
            col_label: v.index,
            col_values: v.values
        })
    else:
        v = df[col_label].value_counts()
        new2 = pd.DataFrame({
            col_label: v.index,
            col_values: v.values
        })
    fig = makepie(new2['mark'],new2['Count'],'Distribucion de notas')
    
    return fig


@app.callback(
    Output("output-data-upload", "children"),
    [Input("stored-data", "data")],
)
def update_table(data):
    table = html.Div()
    df = pd.DataFrame(data)

    table = html.Div(
        [
            html.H5('Datos:'),
            dash_table.DataTable(
                data=df.to_dict('rows'), 
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
            ),
            html.Hr(),
        ]
    )

    return table

@app.callback(
    Output("course-dropdown", "options"),
    [Input("stored-data", "data")],
)
def update_optcourse(data):
    df=pd.DataFrame(data)
    return [{'label':x, 'value':x} for x in sorted(df['course'].unique())]

@app.callback(
    Output("barchart", "figure"),
    [Input("stored-data", "data"),
    Input('course-dropdown', 'value'),
    Input('variable-dropdown', 'value'),],
)
def update_bar(data,curso,variable):
    df = pd.DataFrame(data)
    col_label = variable
    col_values = "Count"
    if(curso !=None):
        df = df[df['course'].isin([curso])]
        v=df[col_label].value_counts()
        new2 = pd.DataFrame({
            col_label: v.index,
            col_values: v.values
        })
    else:
        v = df[col_label].value_counts()
        new2 = pd.DataFrame({
            col_label: v.index,
            col_values: v.values
        })
    fig = makepie(new2[col_label],new2[col_values],'Distribucion de: '+col_label)
    
    return fig

@app.callback(
    Output("matrix", "figure"), 
    Input("stored-data", "data"),
    Input('course-dropdown', 'value'),)
def update_matrix(data,curso):
    df = pd.DataFrame(data)    
    if(curso !=None):
        df = df[df['course'].isin([curso])]
    df=df.iloc[:,1:]    
    labels=df.columns
    fig = px.scatter_matrix(df, dimensions=labels,width=1150,height=1150,)
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    return fig

@app.callback(
    Output("matrix2", "figure"),
    Output("feature_graph", "figure"),
    Input("stored-data", "data"),)
def update_matrix2(data):
    df = pd.DataFrame(data)
    df2=df.copy()
    df=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2, 'FAIL':0, 'PASS':1, 'GOOD':2, 'EXCELLENT':3})
    
    return corelationMatrix(df),featureImportance(df)


@app.callback(
    Output("page-content", "children"),
    Output('upload-div', 'hidden'),    
    Output("alert-auto", "children"),
    Output("alert-auto", "is_open"),
    [Input("stored-data", "data"),]
)
def errorData(data):
    if data==None:
        return pages.home.layout(), False, "No se han añadido los datos para realizarlas las funcionalidades, vuelve a la pantalla de inicio",True
    



