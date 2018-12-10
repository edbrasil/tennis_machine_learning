# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 15:34:52 2018

@author: edbras
"""

import pandas as pd
import numpy as np

"""
Import data
Returns: X and y for modeling
"""
def data_prep_func(df, X_list=None):
   
    """
    Fill missing values
    """
    df[['P Titles','P Points','P ELO Points']] = df[['P Titles','P Points','P ELO Points']].fillna(0)
    
    df['P Rank'].fillna(np.max(df['P Rank']) + 10, inplace=True)
    df['P ELO Rank'].fillna(np.max(df['P ELO Rank']) + 20, inplace=True)
    df['P ELO Rank'].fillna(1000,inplace=True)
    df['P Best Rank'].fillna(np.max(df['P Best Rank']) + 20, inplace=True)
    df['P Handed'].fillna('Right-handed', inplace=True)
    
    df_bd_mode = df['P Best Date'].mode().iloc[0]
    df['P Best Date'].fillna(df_bd_mode, inplace=True)

    df['P Fav Surface'].fillna('None', inplace=True)    
    df['P Fav Surface'] = df['P Fav Surface'].str.split().str.get(0)
    #df['P Fav Surface'].value_counts()
    
    df_b_mode = df['P Backhand'].mode().iloc[0]
    df['P Backhand'] = df['P Backhand'].fillna(df_b_mode)
    
    """
    For simplicity, extract year from Best Date
    """
    df['P Best Date'] = pd.to_datetime(df['P Best Date']).dt.year
    
    """
    Add match_id
    """
    df['MatchID'] = (df.index - (df.index % 2)) / 2
    df['PlayerID'] = df.index % 2
    
    """
    Group by match_id
    """
    df1 = df.pivot(index='MatchID', columns = 'PlayerID' )
    df1.columns = df1.columns.map('{0[0]}_{0[1]}'.format)
    
    """
    Drop irrelevant/redundant columns
    """
    df1.drop(['P Full_0','P Full_1','Player Win_1','Round_1', 'Tournament_1',\
              'Court_1'], axis=1, inplace=True )
    
    #Remove win from head-to-head since stats are drawn post-tournament
    if not pd.isnull(df1['Player Win_0'].iloc[0]):
        df1['P H2H_0'] = df1['P H2H_0'] - df1['Player Win_0']
        df1['P H2H_1'] = df1['P H2H_1'] - (1 - df1['Player Win_0'])
        
    """
    Dummy variables
    """
    df1 = pd.get_dummies(df1, columns=['P Fav Surface_0', 'P Fav Surface_1', \
                                       'P Backhand_0', 'P Backhand_1', \
                                       'P Handed_0', 'P Handed_1', 'Round_0',\
                                       'Tournament_0','Court_0' ], drop_first = True)
    
    if X_list != None:
        miss_list = np.setdiff1d(X_list, df1.columns.values)
        for var in miss_list:
            pieces = var.split("_")
            if df[pieces[0]][int(pieces[1])] == pieces[2]:
                df1[var] = 1
            else:
                df1[var] = 0
    
    """
    Create X and y
    """
    y = df1['Player Win_0']
    X = df1.drop(['Player Win_0', 'Player_0', 'Player_1'], axis=1)
    #print(X)
    
    return X, y