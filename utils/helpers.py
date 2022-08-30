import plotly.graph_objects as go
from sklearn.metrics import classification_report as classificationreport

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    It takes a model, training data, and test data, fits the model to the training data, makes
    predictions on the test data, and returns a classification report
    
    :param model: the model to be evaluated
    :param X_train: The training data
    :param y_train: The training labels
    :param X_test: The test data
    :param y_test: the actual values of the target variable
    :return: A dictionary with the precision, recall, f1-score, and support for each class.
    """
    model = model
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    report = classificationreport(y_test, y_pred, target_names= ["0", "1"], output_dict=True)

    return report

def create_heatmap(df):
    """
    It takes a dataframe as input and returns a heatmap figure
    
    :param df: the dataframe that contains the data to be plotted
    :return: A figure object
    """

    # Creating a heatmap figure.
    fig = go.Figure(data=go.Heatmap(
                       z=df.values.tolist(),
                       x=df.columns,
                        y = df.index.values.tolist(),
                       hoverongaps = False,
                        xgap = 3,
                        ygap = 3,
                        colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
                        ),
                       )
    return fig
