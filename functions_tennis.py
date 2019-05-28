# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 11:40:54 2018

@author: edbras
"""
"""
Import libraries
"""
import pandas as pd
#from logistic_regression import LogRegTennis
from getData_Full import wrapper
from data_prep import data_prep_func
from keras.models import load_model
from sklearn.externals import joblib

"""
Used by currentRank to determine if field is 
missing
"""
def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

    #build logic for choosing winner
    #available attributes: vs (Names), H2H, Age, Country, Birthplace,
    #                      Residence, Height, Weight, Plays, Backhand,
    #                      Favorite Surface, Coach, Turned Pro, Seasons
    #                      Active, Prize Money, Wikipedia, Web Site,
    #                      Facebook, Twitter, Nicknames, Titles, Grand Slams
    #                      Tour Finals, Masters, Current Rank, Best Rank
    #                      Current Elo Rank, Best Elo Rank, Peak Elo Rating,
    #                      GOAT Rank, Weeks at No. 1
    
"""
    Example:
        if df_h2h.loc["H2H"][1] > print(df_h2h.loc["H2H"][2]:
            winner = df_h2h.loc["vs"][1]
        elif df_h2h.loc["H2H"][2] > print(df_h2h.loc["H2H"][1]):
            winner = df_h2h.loc["vs"][2]
"""
    
def currentRank(rank, current_rank):
    
    if isFloat(rank) :
        current_rank.append(10000)
    else:
        current_rank.append(int(rank.split(" ",1)[0]))

def ModelRank(p_dict, model_file, pasttourn=True):
    logreg_cv = joblib.load(model_file)    
    wrapper(p_dict, type = 'dict', out_file = '_temp.xls',
        tourn = 'FRE', court = 'C', rd = list(p_dict.keys())[0], all_rounds = False) 
    
    df_t = pd.read_excel('_temp.xls', header = 0, index_col = 0)
    
    #global X_test
    X_test, y_test = data_prep_func(df_t, X_list="X_list_logreg.save", full_data=False
                                    , drop_extra=False, modtype='logreg', pasttourn=pasttourn)
    
    y_pred = logreg_cv.predict(X_test)
    #y_pred predicts whether player 0 wins (1) or not (0)
    #therefore return (1- y_pred ) to decide which player wins
    return (1 - y_pred[0])


def NeuNetRank(p_dict, pasttourn = True):
    model = load_model('model_50_2.h5')
    wrapper(p_dict, type = 'dict', out_file = '_temp.xls',
            tourn = 'FRE', court = 'C', rd = list(p_dict.keys())[0], all_rounds = False) 

    df_t = pd.read_excel('_temp.xls', header = 0, index_col = 0)

    #global X_test
    X_test, y_test = data_prep_func(df_t, X_list="X_list_neunet.save", full_data=False
                                    , drop_extra=True, pasttourn = pasttourn)

    y_pred = model.predict(X_test)
    #print(y_pred)
    #print(np.rint(y_pred))
    return int(round(y_pred.item(0)))
    
#p_dict = {'r1': ['M Moraing', 'D Schwartzman']}
#ModelRank(p_dict,"logreg_new.h5", pasttourn=False)
#    


