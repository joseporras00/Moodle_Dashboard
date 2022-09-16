import json
import lightgbm as lgb
import plotly.express as px
import plotly.graph_objs as go
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split,StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score,accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
from utils.figures import *
from data_reader import *
import joblib
from app import app

def make_gridSearch(model,X,y,splits):
    """
    This function takes in a model, X, y, and the number of splits for cross validation. It then creates
    a dictionary of parameters for each model, and then uses GridSearchCV to find the best parameters
    for each model
    
    :param model: The model you want to use
    :param X: The input data
    :param y: The target variable
    :param splits: number of splits for cross validation
    :return: The best estimator from the grid search.
    """
    param_grid={}
    #Assigning the model, and it also assigning the parameters for the model.
    if model == 'GNB':
        model = GaussianNB()
        
    elif model == 'SVC':
        param_grid = {'kernel': ['rbf', 'linear'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]}
        model = SVC(probability=True)
        
    elif model == 'LGBM':
        param_grid = {'learning_rate': [0.005, 0.01],'n_estimators': [8,16,24],'num_leaves': [6,8,12,16], 
                      'boosting_type' : ['gbdt', 'dart'],'max_bin':[255, 510]}
        model = lgb.LGBMClassifier()
        
    elif model == 'Logistic':
        model = LogisticRegression()
        param_grid = {'penalty': ['l1','l2'], 'tol' : [1e-4,1e-5], 'max_iter' : [10,100,1000], 
                      'fit_intercept' : [True, False]}
        
    elif model == 'KNN':
        model = KNeighborsClassifier()
        param_grid = {'n_neighbors' : [5,10,20],'weights': ['uniform','distance'], 
                      'algorithm' : ['ball_tree', 'kd_tree', 'brute'],'p' : [1,2,3]}
        
    elif model == 'Random Forest':
        param_grid = {'n_estimators':[10,20,100],'max_features':[0.5,1.0],
                      'criterion' : ['gini','entropy'],'max_depth': [None,100,200]}
        model = RandomForestClassifier()
        
    elif model == 'DT':
        param_grid = {'max_features': ['auto', 'sqrt', 'log2'],'ccp_alpha': [0.1, .01, .001],
              'max_depth' : [5, 6, 7, 8, 9],'criterion' :['gini', 'entropy']}
        model=tree.DecisionTreeClassifier()        
        
    elif model == 'MLP':
        param_grid = {'activation' : ['logistic','tanh','relu'],'hidden_layer_sizes' : [(5,),(10,)], 
                      'max_iter' : [200,1000],'alpha' : [0.0001,0.0005]}
        model = MLPClassifier()
        
    else:
        param_grid= {'n_estimators' : [50,100,200],'random_state' : [None], 
                     'learning_rate' : [1.,0.8,0.5],'algorithm' : ['SAMME','SAMME.R']}
        model = AdaBoostClassifier()
            
    # Using the GridSearchCV function to find the best parameters for the model.
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=splits, verbose=True)
    grid_search.fit(X,y)
    final_model = grid_search.best_estimator_
    
    return final_model

def buildModel(df2, y_v, X_v,slider,splits, model):
        """
        It takes a dataframe, a list of features, a list of target variables, a slider value, a number of
        splits for the cross validation, and a model, and returns the result metrics and figures
        
        :param df2: the dataframe that contains the data
        :param y_v: The name of the column that contains the target variable
        :param X_v: list of features to use in the model
        :param slider: the percentage of the data to be used for training
        :param splits: number of splits for the cross validation
        :param model: the model to be trained
        :return: the precision, recall, accuracy, f1, fig_precision, fig_m, reporte
        """
        # Replacing the values of the data to numeric.
        df=df2.copy()
        df=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2})
        # Taking the columns from the dataframe that are in the list X_v and y_v, and assigning them to X and y.
        X=df[X_v]
        y=df[y_v]  
        target_names=df['mark'].unique()
        # Using the function make_gridSearch to find the best parameters for the model.
        model=make_gridSearch(model,X,y,splits)   
        
        # Splitting the data into training and testing data.
        trainX, testX, trainy, testy = train_test_split(X, y, train_size= slider/100)  
        model.feature_names=list(X_v)
        
        # Predicting the probability of the model.
        lr_probs = model.predict_proba(testX)
        lr_probs = lr_probs[:, 1] 
        # Predicting the values of the target variable for the test data.
        yhat = model.predict(testX)                         
                
        # Creating a histogram of the predicted probabilities.
        fig_precision = px.histogram(
                x = lr_probs, color=testy, nbins=50,
                labels=dict(color='True Labels', x='Score')
        )
                
        # Calculating the metrics of the model.
        precision=round(precision_score(testy, yhat,average='micro'),2)
        recall=round(recall_score(testy, yhat,average='micro'),2)
        accuracy=round(accuracy_score(testy, yhat)*100,1)
        f1=round(f1_score(testy, yhat,average='micro'),2)
                
        # Creating a confusion matrix and a heatmap of the confusion matrix.
        confusion_m=confusion_matrix(testy, yhat)
        fig_m = go.Figure(data=go.Heatmap(
                       z=confusion_m,
                       x=target_names,
                       y =target_names,
                       hoverongaps = False,
                        xgap = 3,
                        ygap = 3,
                        colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
                        ),
                       )                
        
        # Saving the model in the server.
        export_model(model)
        
        # Creating a classification report for the model.
        reporte=classification_report(testy, yhat,target_names=target_names)
                
        return precision, recall, accuracy, f1, fig_precision, fig_m, reporte
    
    
def export_model(model):
    """
    It saves a model in the server
    
    :param model: The model to be saved
    """
    joblib.dump(model, open('./assets/my_model.joblib', 'wb'))
           