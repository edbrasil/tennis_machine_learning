# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 15:32:48 2018

@author: edbras
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 13:33:53 2018

@author: edbras
"""
"""
Use 8 training tournaments (1016 matches) to train
a logistic regression using a 5-fold CV Grid Search
"""

from data_prep import data_prep_func
#import numpy as np
import pandas as pd


# Import necessary modules
# Import random forest classifer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
#from sklearn.externals import joblib
import joblib

#Training tournaments

tourn_list = ['U2016','A2017','F2017','W2017', 'U2017','A2018','F2018','W2018','U2018','A2019','F2019','W2019','U2019']
df_list = []

for f in tourn_list:
    df_list.append(pd.read_excel('./data/data_'+f+'.xls', header = 0, index_col = 0))

df_train = pd.concat(df_list, ignore_index = True)

X_train, y_train = data_prep_func(df_train, modtype="logreg")
X_list = list(X_train.columns.values)
joblib.dump(X_list, "X_list_logreg.save")

# Setup the hyperparameter grid
n_space = range(10,100,10)
depth_space = range(1,9)
param_grid = {'n_estimators': n_space, 
              'max_depth': depth_space,
              'criterion': ['gini', 'entropy']}

# Instantiate a logistic regression classifier: logreg
ranfor = RandomForestClassifier()

# Instantiate the GridSearchCV object: logreg_cv
ranfor_cv = GridSearchCV(ranfor, param_grid, cv=5)

# Fit it to the data
ranfor_cv.fit(X_train, y_train)

# Print the tuned parameters and score
print("Tuned Random Forest Parameters: {}".format(ranfor_cv.best_params_)) 
print("Best score is {}".format(ranfor_cv.best_score_))

#print(dict(zip(X_list, ranfor.best_estimator_.coef_.tolist()[0])))

joblib.dump(ranfor_cv, "ranfor_new.h5")

"""
Display confusion matrix, classification report and prediction results
"""
    
#     Check on validation
from sklearn.metrics import classification_report, confusion_matrix

#Use US Open 2018 as testing
df_U8 = pd.read_excel('./data/data_U2018.xls', header = 0, index_col = 0)
    
X_test, y_test = data_prep_func(df_U8, X_list="X_list_logreg.save", full_data=False
                                    , drop_extra=False, modtype='logreg')    
    
y_pred = ranfor_cv.predict(X_test)
    
#     Compute and print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
    
    
    #Display results for visual inspection
df_U8['MatchID'] = (df_U8.index - (df_U8.index % 2)) / 2
df_U8['PlayerID'] = df_U8.index % 2
#    
df8 = df_U8.pivot(index='MatchID', columns = 'PlayerID')
df8.columns = df8.columns.map('{0[0]}_{0[1]}'.format)
    
df8['predictions'] = y_pred
print(df8[['Player_0','Player_1','Player Win_0','predictions']])
