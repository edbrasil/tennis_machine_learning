# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:01:10 2018

@author: edbras
"""

#import numpy as np
import pandas as pd
from getBracket import getBracket
from getHeadToHead import getH2H
from functions_tennis import currentRank
import json
#from functions_tennis import isFloat

"""
Loop over data frame, need two player names at a time
Player names should be stored in df_r1[0:127]
df_in[0 plays 1, etc]
"""

#set new_bracket to True to create the DataFrame from scratch
#otherwise must have the bracket.xls file in the same directory
df_r1 = getBracket(new_bracket = False)

print (df_r1)

def nextRound(df_r):
    r2 = []

    num_players = min([int(df_r["Full Name"].count()),128])
    #num_players = 16 #For troubleshooting only    

    for i in range(0, num_players, 2):
        player1 = df_r.iloc[i]["Full Name"].replace(" ","%20")
        player2 = df_r.iloc[i+1]["Full Name"].replace(" ","%20")
        #print("Player 1: " + player1)
        #print("Player 2: " + player2)
        df_h2h = getH2H(player1,player2)
        
        current_rank = []
        currentRank(df_h2h.loc["Current Rank"][1],current_rank)
        currentRank(df_h2h.loc["Current Rank"][2],current_rank)
        #print(current_rank)
    
        if current_rank[0] < current_rank[1]:
            #print(df_h2h.loc["vs"][1])
            r2.append([df_r.iloc[i]["Name"],df_r.iloc[i]["Full Name"]])
        else:
            #print(df_h2h.loc["vs"][2])
            r2.append([df_r.iloc[i+1]["Name"],df_r.iloc[i+1]["Full Name"]])
        
    df_r2 = pd.DataFrame(r2)
    df_r2.columns= ["Name","Full Name"]
    return df_r2

def loopRounds(in_df, r_name):
    out_df = nextRound(in_df)
    print(r_name + ":")
    print(out_df)
    out_df.to_json(r_name.replace(" ","") + ".json",orient="values")
    return out_df

df_r1.to_json("Round1.json",orient="values")
df_r2 = loopRounds(df_r1, "Round 2")
df_r3 = loopRounds(df_r2, "Round 3")
df_r4 = loopRounds(df_r3, "Round 4")
df_q = loopRounds(df_r4, "Quarterfinals")
df_s = loopRounds(df_q, "Semifinals")
df_f = loopRounds(df_s, "Final")
df_w = loopRounds(df_f, "Winner")

dict = {"Round 1" : df_r1.values.tolist(),
        "Round 2" : df_r2.values.tolist(),
        "Round 3" : df_r3.values.tolist(),
        "Round 4" : df_r4.values.tolist(),
        "Quarterfinal" : df_q.values.tolist(),
        "Semifinal" : df_s.values.tolist(),
        "Final" : df_f.values.tolist(),
        "Winner" : df_w.values.tolist()}

with open('Picks.json', 'w') as fp:
    json.dump(dict, fp)
