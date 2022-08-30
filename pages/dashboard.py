from matplotlib.pyplot import figure
import plotly.graph_objs as go
from data_reader import *

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from app import app
from data_reader import *
from utils.helpers import *
from utils.figures import *
import pages
import pandas as pd
import plotly.express as px


# A CSS file that is used to style the app.
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# A dictionary that contains the colors that are used in the app.
colors = {"graphBackground": "#F5F5F5", "background": "#ffffff", "text": "#000000"}
  
def layout():
    return [
        html.Div(
            [   
                dbc.Row([
                    html.Div(id="output-data-upload"),
                ]),
                dbc.Row([
                    dbc.Col([
                         html.Div([
                            # A dropdown menu that allows you to select a course.
                            html.H5('Select a course'),
                            dcc.Dropdown(id='course-dropdown',
                                multi=False,
                                clearable=True,
                                value=None,
                            ),                                 
                            dbc.Spinner(dcc.Graph(id="Mygraph")),
                        ]),
                    ]),              
                    dbc.Col([
                        # A dropdown menu that allows you to select a variable of the data.
                        html.H5('Select a variable'),
                        dcc.Dropdown(id='variable-dropdown',
                            multi=False,
                            clearable=False,
                        ), 
                        dbc.Spinner(dcc.Graph(id="pie2")),
                    ]),
                ]),            
                html.Br(),               
                dbc.Row([
                    html.Div([
                        html.H5("Scatter Matrix:"),
                        dbc.Spinner(dcc.Graph(id='matrix')),
                    ]),
                ]),
                html.Br(),
                dbc.Row([
                    html.Div([
                        html.H5("Correlation Matrix:"),
                        dbc.Spinner(dcc.Graph(id='matrix2')),
                    ]),
                ]),
                html.Br(),
                dbc.Row([
                    html.Div([
                        html.H5("Features importance:"),
                        dbc.Spinner(dcc.Graph(id='feature_graph')),
                    ]),
                ]),
                     
            ]
        )
    ]
        
        
@app.callback(Output('Mygraph', 'figure'),
    [
    Input('stored-data', 'data'),
    Input('course-dropdown', 'value'),
])
def update_graph(data,course):
    """
    It takes a dataframe, a column name, and a value, and returns a pie chart of the counts of the
    values in the column 'mark'
    
    :param data: the dataframe that contains the data
    :param curso: the course name
    :return: A figure object.
    """
    df = pd.DataFrame(data)
    col_label = "mark"
    col_values = "Count"
    
    # Filtering the dataframe by the course number.
    if(course !=None):
        df = df[df['course'].isin([course])]
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
        
    # Creating a pie chart
    fig = makepie(new2['mark'],new2['Count'],'Marks Distribution')
    
    return fig


@app.callback(
    Output("output-data-upload", "children"),
    [Input("stored-data", "data")],
)
def update_table(data):
    """
    It takes a the stored data as a dataframe and returns a dash table
    
    :param data: The data to be displayed in the table
    :return: A Div containing a DataTable
    """
    table = html.Div()
    df = pd.DataFrame(data)

    table = html.Div(
        [
            html.H5('Data:'),
            dash_table.DataTable(
                data=df.to_dict('rows'), 
                columns=[{"name": i, "id": i} for i in df.columns],
                # Making the table scrollable.
                style_table={'overflowX': 'scroll'},
                # It allows you to filter the data in the table.
                filter_action='native',
                # It allows you to sort the data in the table by clicking on the column name.
                sort_action='native',
                sort_mode='multi',
                column_selectable='single',
                selected_columns=[],
                selected_rows=[],
                # It allows you to navigate through the pages of the table.
                page_action='native',
                page_current= 0,
                # Setting the number of rows that are displayed in the table.
                page_size= 20,
                # Changing the background color of the odd rows in the table.
                style_data_conditional=[        
                    {'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}
                ],
            ),
            html.Br(),
        ]
    )

    return table

@app.callback(
    Output("course-dropdown", "options"),
    [Input("stored-data", "data")],
)
def update_optcourse(data):
    """
    It takes the stored data as a dataframe and returns a list of dictionaries, where each dictionary contains a
    label and a value. 
    
    The label is the unique course name, and the value is the same as the label. 
    
    The list of dictionaries is sorted alphabetically
    
    :param data: the dataframe that contains the data that you want to use to update the dropdown
    :return: A list of dictionaries about the courses.
    """
    df=pd.DataFrame(data)
    return [{'label':x, 'value':x} for x in sorted(df['course'].unique())]

@app.callback(
    Output("variable-dropdown", "options"),
    Output("variable-dropdown", "value"),
    [Input("stored-data", "data")],
)
def update_optvariables(data):
    """
    The function returns the column names of the dataframe as the options for the dropdown 
    and the second column name as the default value
    
    :param data: the dataframe that is stored in the hidden div
    :return: The first value is the list of options for the dropdown. The second value is the default
    value for the dropdown.
    """    
    df=pd.DataFrame(data)
    return df.columns.values,df.columns.values[1]

@app.callback(
    Output("pie2", "figure"),
    [Input("stored-data", "data"),
    Input('course-dropdown', 'value'),
    Input('variable-dropdown', 'value'),],
)
def update_bar(data,course,variable):
    """
    It takes in a dataframe, a course, and a variable, and returns a pie figure
    
    :param data: the dataframe
    :param curso: the course you want to filter by
    :param variable: the column name of the dataframe that you want to plot
    :return: A figure object
    """
    df = pd.DataFrame(data)
    col_label = variable
    col_values = "Count"
    
    # Filtering the dataframe by the course name.
    if(course !=None):
        df = df[df['course'].isin([course])]
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
        
    # Creating a pie chart.
    fig = makepie(new2[col_label],new2[col_values],col_label+' distribution: ')
    
    return fig

@app.callback(
    Output("matrix", "figure"), 
    Input("stored-data", "data"),
    Input('course-dropdown', 'value'),)
def update_matrix(data,course):
    """
    It takes a dataframe and a course name as input, filters the dataframe by the course name, and
    returns a scatter matrix plot of the filtered dataframe
    
    :param data: the dataframe
    :param curso: the course to filter by
    :return: A figure object
    """
    df = pd.DataFrame(data)    
    
    # Filtering the dataframe by the course name.
    if(course !=None):
        df = df[df['course'].isin([course])]
    df=df.iloc[:,1:]    
    labels=df.columns
    
    # Creating a scatter matrix plot.
    fig = px.scatter_matrix(df, dimensions=labels,width=1150,height=1150)
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    return fig

@app.callback(
    Output("matrix2", "figure"),
    Output("feature_graph", "figure"),
    Input("stored-data", "data"),)
def update_matrix2(data):
    """
    It takes a dataframe, then returns the correlation matrix and feature importance graphs
    
    :param data: the stored data in the app
    :return: the corelation matrix and feature importance graphs
    """
    df = pd.DataFrame(data)
    df=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2, 'FAIL':0, 'PASS':1, 'GOOD':2, 'EXCELLENT':3})
    
    return corelationMatrix(df),featureImportance(df)


    



