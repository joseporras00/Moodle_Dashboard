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
    X = df.iloc[:,:-1]
    y = df.iloc[:,-1]
    trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.5, random_state=2)
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(trainX, trainy)
    
    sorted_idx = rf.feature_importances_.argsort()
    fig_featureImp = px.bar(df.columns[sorted_idx], rf.feature_importances_[sorted_idx],
    title= 'Variable Importance')
    return fig_featureImp


def corelationMatrix(df):
    corr_matrix = df.corr()
    fig = px.imshow(corr_matrix, title= "Correlation Matrix")
    return fig

def serve_bar(df):
    x_axis='student_id'
    y_axis='n_quiz_a'
    return px.bar(
            data_frame=df,
            x=x_axis,
            y=y_axis,
            title=y_axis+': by '+x_axis,
            )


def serve_pie_pass(df):
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
                "title" : dict(text ="Distribuci??n notas",
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

def serve_prediction_plot(df):
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

    layout = go.Layout(
        xaxis=dict(
            # scaleanchor="y",
            # scaleratio=1,
            ticks='',
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
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

    data = [trace2, trace3]
    figure = go.Figure(data=data, layout=layout)

    return figure


def serve_roc_curve(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model=SVC()
    model.fit(X_train, y_train)
    decision_test = model.decision_function(X_test)
    fpr, tpr, threshold = metrics.roc_curve(y_test, decision_test)

    # AUC Score
    auc_score = metrics.roc_auc_score(y_true=y_test, y_score=decision_test)

    trace0 = go.Scatter(
        x=fpr,
        y=tpr,
        mode='lines',
        name='Test Data',
    )

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
    y_pred_test = y_pred.astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix SVC',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_lgb(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = lgb.LGBMClassifier(n_estimators=1000,max_depth=4,random_state=22)
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix LGB',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_rf(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = RandomForestClassifier()
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix RF',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_knn(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix KNN',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_GB(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = GaussianNB()
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix GB',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_ADA(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = AdaBoostClassifier()
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix ADAB',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure

def serve_pie_confusion_matrix_logr(df):
    X = df.iloc[:,:-1].values
    y = df.iloc[:,-1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train,y_train)
    y_pred_test = (model.predict(X_test)).astype(int)

    matrix = metrics.confusion_matrix(y_true=y_test, y_pred=y_pred_test)
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

    layout = go.Layout(
        title=f'Confusion Matrix LR',
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0)',
            orientation='h'
        )
    )

    data = [trace0]
    figure = go.Figure(data=data, layout=layout)

    return figure


