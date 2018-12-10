# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 11:40:54 2018

@author: edbras
"""
"""
Import libraries
"""
import pandas as pd
from logistic_regression import LogRegTennis
from getData_Full import wrapper
from data_prep import data_prep_func

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

def logRegRank(p_dict, needTrain=False):
    #Only run logistic regression the first round
    global X_list
    try:
        X_list
    except NameError:
        #Training tournaments
        
        tourn_list = ['U2017','A2018','F2018','W2018']
        df_list = []
        
        for f in tourn_list:
            df_list.append(pd.read_excel('data_'+f+'.xls', header = 0, index_col = 0))
        
        df = pd.concat(df_list, ignore_index = True)
        
        global logreg_cv
        #global X_list
        logreg_cv, X_list = LogRegTennis(df)
        
    wrapper(p_dict, type = 'dict', out_file = '_temp.xls',
        tourn = 'US', court = 'H', all_rounds = False) 
    
    df_t = pd.read_excel('_temp.xls', header = 0, index_col = 0)
    
    #global X_test
    X_test, y_test = data_prep_func(df_t, X_list)
    
    y_pred = logreg_cv.predict(X_test)
    #y_pred predicts whether player 0 wins (1) or not (0)
    #therefore return (1- y_pred ) to decide which player wins
    return (1 - y_pred[0])
    
p_dict = {'r1': ['C Altamirano', 'U Humbert']}
logRegRank(p_dict, needTrain=False)
#    


