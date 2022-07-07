import plotly.graph_objects as go
from sklearn.metrics import classification_report as classificationreport

def evaluate_model(model, X_train, y_train, X_test, y_test):
    model = model
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    report = classificationreport(y_test, y_pred, target_names= ["0", "1"], output_dict=True)

    return report

def create_heatmap(df):

    fig = go.Figure(data=go.Heatmap(
                       z=df.values.tolist(),
                       x=df.columns,
                       #y=[classifier for classifier in df.index.values.tolist()],
                        y = df.index.values.tolist(),
                       hoverongaps = False,
                        xgap = 3,
                        ygap = 3,
                        colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
                        ),
                       )
    return fig
