# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 11:40:54 2018

@author: edbras
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