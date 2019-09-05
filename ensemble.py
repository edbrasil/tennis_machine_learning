# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:27:13 2019

@author: edbras
"""

from mlxtend.classifier import EnsembleVoteClassifier
import joblib
#from keras.models import load_model
import pandas as pd
from data_prep import data_prep_func

logreg = joblib.load("logreg_new.h5")
#neunet = load_model("model_50_2.h5")
ranfor = joblib.load("ranfor_new.h5")
xg_cl = joblib.load("xg_cl.h5") 

eclf = EnsembleVoteClassifier(clfs=[logreg, ranfor, xg_cl],
                              weights=[1,1,1],
                              refit=False)

tourn_list = ['U2016','A2017','F2017','W2017','U2017','A2018','F2018','W2018','U2018','A2019','F2019','W2019']
df_list = []

for f in tourn_list:
    df_list.append(pd.read_excel('./data/data_'+f+'.xls', header = 0, index_col = 0))

df_train = pd.concat(df_list, ignore_index = True)

#def NeuNetTennis(df_train):
X_train, y_train = data_prep_func(df_train, full_data=True, drop_extra = True)

joblib.dump(eclf.fit(X_train, y_train), "eclf.h5")
