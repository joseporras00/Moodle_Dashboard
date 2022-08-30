import colorlover as cl
import plotly.graph_objs as go
import numpy as np
from sklearn import metrics
from dash import dcc
import pandas as pd
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
import plotly.express as px

def featureImportance(df):
    """
    The function takes a dataframe as input, splits it into training and testing sets, fits a random
    forest model, and returns a plot of the feature importances
    
    :param df: the dataframe you want to use
    :return: A plotly figure object
    """
   # Splitting the data into training and testing sets and fitting a random forest model
    X = df.iloc[:,:-1].copy()
    y = df.iloc[:,-1].copy()
    trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(trainX, trainy)
    
    # Sorting the features by their importance, and then plotting them in a bar chart.
    sorted_idx = rf.feature_importances_.argsort()
    fig_featureImp = px.bar(df.columns[sorted_idx], rf.feature_importances_[sorted_idx])
    return fig_featureImp


def corelationMatrix(df):
    """
    It takes a dataframe as input and returns a plotly figure of the correlation matrix
    
    :param df: The dataframe you want to plot
    :return: A correlation matrix
    """
    # Creating a correlation matrix and then plotting it using plotly express.
    corr_matrix = df.corr()
    fig = px.imshow(corr_matrix)
    return fig

def makepie(labels,values,text):
    """
    It takes in three arguments, labels, values, and text, and returns a pie figure object
    
    :param labels: list of labels
    :param values: A list of values for each slice of the pie
    :param texto: the title of the pie chart
    :return: A dictionary with the data and layout for a pie chart.
    """
    fig= go.figure = {
            # Creating a dictionary with the data and layout for a pie chart.
            "data": [
                {
                "labels":labels,
                "values":values,
                # Information displayed when the user hovers over a slice of the pie chart.
                "hoverinfo":"label+percent",
                # The size of the hole in the middle of the pie chart.
                "hole": .7,
                # Telling plotly to make a pie chart.
                "type": "pie",
                'marker': {'colors': [
                    '#FB9C34',  
                    '#F48E2C',
                    '#F47C2B',
                    '#EC7C2C'
                    ]
                    },
                # Showing the legend of the plot.
                "showlegend": True
            }],
            # The layout of the pie chart.
            "layout": {
                "title" : dict(text =text,
                          font =dict(
                               size=20,
                               color = 'black')),
                "paper_bgcolor":"#white",
                "showlegend":True,
                'height':500,
                'marker': {'colors': [
                            '#FB9C34',  
                            '#8C5C44',
                            '#F47C2B',
                            '#EC7C2C'
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
                # Setting the legend to white.
                "showlegend": True,
                "legend":dict(fontColor="white",tickfont={'color':'white' }),
                "legenditem": {
                    "textfont": {
                        'color':'white'
                    }
                }
    } }
    return fig

def serve_prediction_plot(df):
    """
    The function takes in a dataframe, splits it into training and testing sets, fits a model, and
    returns a plotly figure object.
    
    :param df: The dataframe that contains the data to be plotted
    :return: A plotly figure object.
    """
    # Splitting the data into training and testing sets and fitting a model.
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model=SVC()
    model.fit(X_train, y_train)
 
    # Get train and test score from model
    y_pred_train = (model.decision_function(X_train)).astype(int)
    y_pred_test = (model.decision_function(X_test)).astype(int)
    train_score = metrics.accuracy_score(y_true=y_train, y_pred=y_pred_train)
    test_score = metrics.accuracy_score(y_true=y_test, y_pred=y_pred_test)

    # Colorscale
    bright_cscale = [[0, '#FF0000'], [1, '#0000FF']]

    colorscale_zip = zip(np.arange(0, 1.01, 1 / 8),
                         cl.scales['9']['div']['RdBu'])
    cscale = list(map(list, colorscale_zip))

    # Create the plot
    # Plot Training Data
    trace2 = go.Scatter(
        x=X_train[:, 0],
        y=y_train[:, 1],
        mode='markers',
        name=f'Training Data (accuracy={train_score:.3f})',
        marker=dict(
            size=10,
            color=y_train,
            colorscale=bright_cscale,
            line=dict(
                width=1
            )
        )
    )

    # Plot Test Data
    trace3 = go.Scatter(
        x=X_test[:, 0],
        y=y_test[:, 1],
        mode='markers',
        name=f'Test Data (accuracy={test_score:.3f})',
        marker=dict(
            size=10,
            symbol='triangle-up',
            color=y_test,
            colorscale=bright_cscale,
            line=dict(
                width=1
            ),
        )
    )

    # Setting the layout of the plot.
    layout = go.Layout(
        # Hiding the x-axis.
        xaxis=dict(
            ticks='',
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        # Hiding the y-axis.
        yaxis=dict(
            ticks='',
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        hovermode='closest',
        legend=dict(x=0, y=-0.01, orientation="h"),
        margin=dict(l=0, r=0, t=0, b=0),
    )

    # Creating a plotly figure object.
    data = [trace2, trace3]
    figure = go.Figure(data=data, layout=layout)

    return figure


def serve_roc_curve(df):
    """
    We take in a dataframe, split it into training and testing data, fit a model, and then plot the ROC
    curve
    
    :param df: The dataframe that contains the data to be plotted
    :return: A plotly figure object
    """
   # Splitting the data into training and testing sets and fitting a model.
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model=SVC()
    model.fit(X_train, y_train)
    
    # Calculating the ROC curve.
    decision_test = model.decision_function(X_test)
    fpr, tpr, threshold = metrics.roc_curve(y_test, decision_test)

    # AUC Score
    auc_score = metrics.roc_auc_score(y_true=y_test, y_score=decision_test)

    # Creating a plotly figure object.
    trace0 = go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name='Test Data',
    )

    # Setting the layout of the plot.
    layout = go.Layout(
        title=f'ROC Curve (AUC = {auc_score:.3f})',
        xaxis=dict(
            title='False Positive Rate'
        ),
        yaxis=dict(
            title='True Positive Rate'
        ),
        legend=dict(x=0, y=1.05, orientation="h"),
        margin=dict(l=50, r=10, t=55, b=40),
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure


def serve_pie_confusion_matrix(y_test, y_pred):
    """
    It takes the true labels and predicted labels as input, and returns a pie chart of the confusion matrix
    
    :param y_test: the actual values of the target variable
    :param y_pred: the predicted values from the model
    :return: A plotly figure object
    """
    # Creating a confusion matrix.
    y_pred_test = y_pred.astype(int)
    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
    
    # Unpacking the confusion matrix.
    tn, fp, fn, tp = matrix.ravel()

    values = [tp, fn, fp, tn]
    label_text = ["True Positive",
                  "False Negative",
                  "False Positive",
                  "True Negative"]
    labels = ["TP", "FN", "FP", "TN"]
    blue = cl.flipper()['seq']['9']['Blues']
    red = cl.flipper()['seq']['9']['Reds']
    colors = [blue[4], blue[1], red[1], red[4]]

    # Creating a pie chart.
    trace0 = go.Pie(
        labels=label_text,
        values=values,
        hoverinfo='label+value+percent',
        textinfo='text+value',
        text=labels,
        sort=False,
        marker=dict(
            colors=colors
        )
    )

    # Setting the layout of the pie chart.
    layout = go.Layout(
        title=f'Confusion Matrix SVC',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    # Creating a plotly figure object.
    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure
