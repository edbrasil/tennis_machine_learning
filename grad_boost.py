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
import numpy as np
import pandas as pd


# Import necessary modules
# Import xgboost
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

#Training tournaments

tourn_list = ['U2016','A2017','F2017','W2017', 'U2017','A2018','F2018','W2018','U2018','A2019','F2019','W2019','U2019']
df_list = []

for f in tourn_list:
    df_list.append(pd.read_excel('./data/data_'+f+'.xls', header = 0, index_col = 0))

df_train = pd.concat(df_list, ignore_index = True)

X, y = data_prep_func(df_train, modtype="logreg")
X_list = list(X.columns.values)
joblib.dump(X_list, "X_list_logreg.save")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

"""
1. SIMPLE
"""
xg_cl = xgb.XGBClassifier(objective='binary:logistic',
                          n_estimators=10)

# Fit it to the data
xg_cl.fit(X_train, y_train)

preds = xg_cl.predict(X_test)
accuracy = float(np.sum(preds==y_test))/y_test.shape[0]

print("accuracy: %f" % (accuracy))
# END SIMPLE

"""
2. CV
"""
cv_dmatrix = xgb.DMatrix(data=X, label=y)

params={"objective":"reg:logistic",
        "max_depth":6,
        "n_estimators":90}

cv_results = xgb.cv(dtrain=cv_dmatrix, params=params, nfold=4,
                    num_boost_round=8, metrics="error",as_pandas=True)

print("Accuracy: %f" %((1-cv_results["test-error-mean"]).iloc[-1]))

#END CV

"""
3. GRID SEARCH
"""
gbm_param_grid = {'objective':['binary:logistic'],
                  'learning_rate':[0.01, 0.1, 0.5, 0.9],
                  'n_estimators':range(170,200,10),
                  'subsample':[0.3, 0.5, 0.9],
                  'max_depth':range(1,5),
                  'eval_metric':['rmse']}

gbm = xgb.XGBClassifier()
grid_mse = GridSearchCV(estimator=gbm, param_grid=gbm_param_grid,
                        cv=4, verbose=1, n_jobs = -1)
grid_mse.fit(X_train,y_train)

print("Best parameters found: ",grid_mse.best_params_) 
print("Lowest RMSE found: ", np.sqrt(np.abs(grid_mse.best_score_))) 

preds = grid_mse.predict(X_test)
accuracy = float(np.sum(preds==y_test))/y_test.shape[0]
print("accuracy: %f" % (accuracy))

#END GRID SEARCH

#print(dict(zip(X_list, ranfor.best_estimator_.coef_.tolist()[0])))

joblib.dump(grid_mse, "xg_cl.h5")

"""
Display confusion matrix, classification report and prediction results
"""
    
#     Check on validation
from sklearn.metrics import classification_report, confusion_matrix

#Use US Open 2018 as testing
#df_U8 = pd.read_excel('./data/data_U2018.xls', header = 0, index_col = 0)
#    
#X_test, y_test = data_prep_func(df_U8, X_list="X_list_logreg.save", full_data=False
#                                    , drop_extra=False, modtype='logreg')    
#    
y_pred = xg_cl.predict(X_test)
    
#     Compute and print the confusion matrix and classification report
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
    
    
#    #Display results for visual inspection
#df_U8['MatchID'] = (df_U8.index - (df_U8.index % 2)) / 2
#df_U8['PlayerID'] = df_U8.index % 2
##    
#df8 = df_U8.pivot(index='MatchID', columns = 'PlayerID')
#df8.columns = df8.columns.map('{0[0]}_{0[1]}'.format)
#    
#df8['predictions'] = y_pred
#print(df8[['Player_0','Player_1','Player Win_0','predictions']])
