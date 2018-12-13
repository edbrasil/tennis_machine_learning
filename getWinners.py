# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:01:10 2018

@author: edbras
"""

"""
Uses getBracket.getBracket and getHeadToHead.getH2H
to pick round by round winners

Current logic: higher ranked player
    This comes from functions_tennis.current__rank

Final result is Picks.json with selected winners
"""

#import numpy as np
import pandas as pd
#from getBracket import getBracket
from getHeadToHead import getH2H
from functions_tennis import currentRank
from functions_tennis import logRegRank
from functions_tennis import NeuNetRank
import json
#from functions_tennis import isFloat

"""
Loop over data frame, need two player names at a time
Player names should be stored in df_r1[0:127]
df_in[0 plays 1, etc]
"""
#global X_list
#get Round 1 from json
json_file = open('C_picks_U2018.json')
json_str = json_file.read()
json_data = json.loads(json_str)
df_r1 = pd.DataFrame(json_data['Round 1'], columns = ["Name"])

df_r1["Full Name"]=""   
df_lu = pd.read_excel("./Excel Files/bracket.xls"
                      ,sheet_name="Sheet1"
                      ,header=0)    

for i in range(128):
    #Player Names
    player_1 = df_r1["Name"][i]
    try:
        df_r1["Full Name"][i] = df_lu["Full Name"].loc[df_lu.loc[df_lu["Name"] == player_1].index].item()
    except ValueError:
        print("Value Error: " + player_1)
#print (df_r1)

"""
Populates next round based on current_rank
Called by following function loopRounds
"""
def nextRound(df_r, r_num, type = 'logreg'):
    r2 = []

    num_players = min([int(df_r["Full Name"].count()),128])
    #num_players = 16 #For troubleshooting only    
    
    for i in range(0, num_players, 2):
        player1 = df_r.iloc[i]["Full Name"].replace(" ","%20")
        player2 = df_r.iloc[i+1]["Full Name"].replace(" ","%20")
        #print("Player 1: " + player1)
        #print("Player 2: " + player2)

        
        if type == 'currank':
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
        elif type == 'logreg':
            p_dict = {'r' + r_num :[df_r.iloc[i]["Name"],
                           df_r.iloc[i+1]["Name"]]}
            winner = logRegRank(p_dict)
            print(df_r.iloc[i+winner]["Name"])
            r2.append([df_r.iloc[i+winner]["Name"],df_r.iloc[i+winner]["Full Name"]])
        elif type == 'neunet':
            p_dict = {'r' + r_num :[df_r.iloc[i]["Name"],
                           df_r.iloc[i+1]["Name"]]}
            winner = NeuNetRank(p_dict)
            print(df_r.iloc[i+winner]["Name"])
            r2.append([df_r.iloc[i+winner]["Name"],df_r.iloc[i+winner]["Full Name"]])   

            
        
    df_r2 = pd.DataFrame(r2)
    df_r2.columns= ["Name","Full Name"]
    return df_r2

"""
Loop Rounds and display round names and resulting DF
Calls nextRound
"""

def loopRounds(in_df, r_name, r_num):
    out_df = nextRound(in_df, r_num, type='logreg')
    print(r_name + ":")
    print(out_df)
    #out_df.to_json(r_name.replace(" ","") + ".json",orient="values")
    return out_df

"""
Get Rounds
"""
#df_r1.to_json("Round1.json",orient="values")
df_r2 = loopRounds(df_r1, "Round 2", "2")
df_r3 = loopRounds(df_r2, "Round 3", "3")
df_r4 = loopRounds(df_r3, "Round 4", "4")
df_q = loopRounds(df_r4, "Quarterfinals", "5")
df_s = loopRounds(df_q, "Semifinals", "6")
df_f = loopRounds(df_s, "Final", "7")
df_w = loopRounds(df_f, "Winner", "8")

"""
Add rounds to Dict and export to 'Picks.json'
"""

out_dict = {"Round 1" : df_r1.values.tolist(),
        "Round 2" : df_r2.values.tolist(),
        "Round 3" : df_r3.values.tolist(),
        "Round 4" : df_r4.values.tolist(),
        "Quarterfinal" : df_q.values.tolist(),
        "Semifinal" : df_s.values.tolist(),
        "Final" : df_f.values.tolist(),
        "Winner" : df_w.values.tolist()}

with open('Picks_logreg2.json', 'w') as fp:
    json.dump(out_dict, fp)
