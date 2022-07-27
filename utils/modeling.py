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
    param_grid={}
    if model == 'GNB':
        model = GaussianNB()
        
    elif model == 'SVC':
        param_grid = {'kernel': ['rbf', 'linear'], 'gamma': [1e-3, 1e-4],'C': [1, 10, 100, 1000]}
        model = SVC()
        
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
            
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=splits, verbose=True)
    grid_search.fit(X,y)
    final_model = grid_search.best_estimator_
    
    return final_model

def buildModel(df2, y_v, X_v,slider,splits, model):
        df=df2
        df=df.replace({'LOW': 0, 'MEDIUM':1, 'HIGH':2})
        X=df[X_v]
        y=df[y_v]  
        
        model=make_gridSearch(model,X,y,splits)   
        
        trainX, testX, trainy, testy = train_test_split(X, y, train_size= slider/100)  
        #model.fit(trainX, trainy)
            
        lr_probs = model.predict_proba(testX)
        yhat = model.predict(testX)            
            
        lr_probs = lr_probs[:, 1]            

            # precision tp / (tp + fp)
        #final_prec.append(round(precision_score(testy, yhat,average='micro'),2))
            # recall: tp / (tp + fn)
        #final_recall.append(round(recall_score(testy, yhat,average='micro'),2))
            
        #final_acu.append(round(accuracy_score(testy, yhat)*100,1))
        #final_f1.append(round(f1_score(testy, yhat,average='micro'),2))
        
                
        fig_precision = px.histogram(
                x = lr_probs, color=testy, nbins=50,
                labels=dict(color='True Labels', x='Score')
        )
        
        precision=round(precision_score(testy, yhat,average='micro'),2)
        recall=round(recall_score(testy, yhat,average='micro'),2)
        accuracy=round(accuracy_score(testy, yhat)*100,1)
        f1=round(f1_score(testy, yhat,average='micro'),2)
                
        confusion_m=confusion_matrix(testy, yhat)
        fig_m = go.Figure(data=go.Heatmap(
                       z=confusion_m,
                       x=['FAIL', 'PASS', 'GOOD', 'EXCELLENT'],
                       y =['FAIL', 'PASS', 'GOOD', 'EXCELLENT'],
                       hoverongaps = False,
                        xgap = 3,
                        ygap = 3,
                        colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
                        ),
                       )
                
        
        exportar_modelo(model)
        
        reporte=classification_report(testy, yhat,target_names=['FAIL', 'PASS', 'GOOD', 'EXCELLENT'])
                
        return precision, recall, accuracy, f1, fig_precision, fig_m, reporte
    
    
def exportar_modelo(model):
    joblib.dump(model, open('./assets/my_model.joblib', 'wb'))
           