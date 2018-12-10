# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 15:17:37 2018

@author: edbras
"""

import pandas as pd
import json
#import codecs
from getHeadToHead import getH2H

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

"""
Gets a dictionary of players per round from the
C_picks JSON or provided list of players
This JSON comes from getCorrect.py
"""
def getData (file_name, all_rounds = False):
    
    def remBracket(rnd, dc):
        lt = []
        for elem in dc[rnd]:
            lt.append(elem[0])
        return lt
        
    #Get Rounds 2 - 7 from correct picks JSON
    json_file = open(file_name,encoding = "utf_8")
    json_str = json_file.read()
    dict2 = json.loads(json_str)
    
    json_file.close()
    
    if all_rounds:
        Rounds = ["Round 1", "Round 2", "Round 3", \
          "Round 4", "Quarterfinal", \
          "Semifinal", "Final", "Winner"]
    else:
        Rounds = ["Round 1"]
    
    p_dict = {}
    
    for i in range(len(Rounds)):
        p_dict["r"+ str(i+1)] = remBracket(Rounds[i], dict2)
    
    return p_dict

"""
Loops over the rounds and gathers required statistics
"""
#print(df_lu["Full Name"].loc[df_lu.loc[df_lu["Name"] == "J Isner"].index].item())
def loopRounds(r_in, r_out, p_dict,df, 
               tourn, court, all_rounds):
    
    data = []
    
    df_lu = pd.read_excel("bracket.xls"
                      ,sheet_name="Sheet1"
                      ,header=0)    
   
    #print (p_dict)
    count = len(p_dict[r_in])
    for i in range(0,count,2):
        #Player Names
        player_1 = p_dict[r_in][i]
        try:
            p1_full = df_lu["Full Name"].loc[df_lu.loc[df_lu["Name"] == player_1].index].item()
        except ValueError:
            print("Value Error: " + player_1)
            
        player_2 = p_dict[r_in][i + 1]
        
        try:
            p2_full = df_lu["Full Name"].loc[df_lu.loc[df_lu["Name"] == player_2].index].item()
        except ValueError:
            print(player_2)
        
        #Winner based on who is in next round
        if all_rounds and r_out != None:
            if player_1 in p_dict[r_out]:
                p1_win = 1
                p2_win = 0
            else:
                p1_win = 0
                p2_win = 1
        else:
            p1_win = None
            p2_win = None
            
        #Other Data
        p1 = p1_full.replace(" ","%20")
        p2 = p2_full.replace(" ","%20")
        df_h2h = getH2H(p1,p2)
        
        #print(df_h2h)
        
        
    #available attributes: vs (Names), H2H, Age, Country, Birthplace,
    #                      Residence, Height, Weight, Plays, Backhand,
    #                      Favorite Surface, Coach, Turned Pro, Seasons,
    #                      Active, Prize Money, Wikipedia, Web Site,
    #                      Facebook, Twitter, Nicknames, Titles, Grand Slams,
    #                      Tour Finals, Masters, Current Rank, Best Rank
    #                      Current Elo Rank, Best Elo Rank, Peak Elo Rating,
    #                      GOAT Rank, Weeks at No. 1

        def getStat(label, i, is_rank = 0):
            if label in df_h2h.index:
                pstat = df_h2h.loc[label][i]
            else:
                pstat = ""
            return pstat
        
        p1_rank = getStat("Current Rank", 1)
        if p1_rank != "" and not isFloat(p1_rank):
            p1_points = p1_rank[p1_rank.find("(")+1:p1_rank.find(")")]
            p1_rank = int(p1_rank.split(" ",1)[0])
        else:
            p1_points = ""
            
        p2_rank = getStat("Current Rank", 2)
        if p2_rank != "" and not isFloat(p2_rank):
            p2_points = p2_rank[p2_rank.find("(")+1:p2_rank.find(")")]
            p2_rank = int(p2_rank.split(" ",1)[0])
        else:
            p2_points = ""
        
        p1_h2h = getStat("H2H", 1)
        if type(p1_h2h) != str:
            p1_h2h = str(p1_h2h.iloc[0])
            
        p2_h2h = getStat("H2H", 2)
        if type(p2_h2h) != str:
            p2_h2h = str(p2_h2h.iloc[0])
        
        p1_surf = getStat("Favorite Surface", 1)
        p2_surf = getStat("Favorite Surface", 2)
        
        p1_titles = getStat("Titles", 1)
        p2_titles = getStat("Titles", 2)
        
        p1_bestrank = getStat("Best Rank", 1)
        p2_bestrank = getStat("Best Rank", 2)
        if p1_bestrank != "" and not isFloat(p1_bestrank):
            p1_bestdate = p1_bestrank[p1_bestrank.find("(")+1:p1_bestrank.find(")")]
            p1_bestrank = int(p1_bestrank.split(" ",1)[0])
        else:
            p1_bestdate = ""
            
        if p2_bestrank != "" and not isFloat(p2_bestrank):
            p2_bestdate = p2_bestrank[p2_bestrank.find("(")+1:p2_bestrank.find(")")]
            p2_bestrank = int(p2_bestrank.split(" ",1)[0])
        else:
            p2_bestdate = ""
        
        p1_elorank = getStat("Current Elo Rank", 1)
        p2_elorank = getStat("Current Elo Rank", 2)
        if not isFloat(p1_elorank) and p1_elorank != "":
            p1_elopoints = p1_elorank[p1_elorank.find("(")+1:p1_elorank.find(")")]
            p1_elorank = int(p1_elorank.split(" ",1)[0])
        else:
            p1_elopoints = ""
            
        if not isFloat(p2_elorank) and p2_elorank != "":
            p2_elopoints = p2_elorank[p2_elorank.find("(")+1:p2_elorank.find(")")]
            p2_elorank = int(p2_elorank.split(" ",1)[0])
        else:
            p2_elopoints = ""
        
        p1_seasons = getStat("Seasons", 1)
        p2_seasons = getStat("Seasons", 2)
        
        p1_back = getStat("Backhand", 1)
        p2_back = getStat("Backhand", 2)
        
        p1_plays = getStat("Plays", 1)
        p2_plays = getStat("Plays", 2)
            
        #Create list of data points for match-up
        vals1 = [player_1, p1_full, 
                p1_rank, p1_points, p1_h2h,
                p1_surf, p1_titles, 
                p1_bestrank, p1_bestdate,
                p1_elorank, p1_elopoints,
                p1_seasons, p1_back, p1_plays,
                p1_win, r_in, tourn, court]
        
        vals2 = [player_2, p2_full, 
                p2_rank, p2_points, p2_h2h,
                p2_surf, p2_titles, 
                p2_bestrank, p2_bestdate,
                p2_elorank, p2_elopoints,
                p2_seasons, p2_back, p2_plays,
                p2_win, r_in, tourn, court]

        data.append(vals1)
        data.append(vals2)
        
        #print(data)
        
        #print(data)
    
    #Feed list into DataFrame    
    df1 = pd.DataFrame(data,columns = ["Player", "P Full", 
                                       "P Rank", "P Points",
                                       "P H2H",
                                       "P Fav Surface", 
                                       "P Titles", "P Best Rank",
                                       "P Best Date",
                                       "P ELO Rank", "P ELO Points",
                                       "P Seasons", "P Backhand", "P Handed",
                                       "Player Win", 
                                       "Round","Tournament", "Court"])
    
    #Add row to full DataFrame   
    df = pd.concat([df,df1])
    return df

def wrapper(file_name = "R1_U2018.json",
            type = 'json',
            out_file = "data_U1_2018.xls",
            tourn = "US",
            court = "H",
            all_rounds = False):
    
    if type == 'json':
        p_dict = getData(file_name, all_rounds)
    else:
        p_dict = file_name
    #print(p_dict)
    
    df = pd.DataFrame()
    for i in range(1,len(p_dict)+1):
        r_in = "r" + str(i)
        #print(r_in)
        if all_rounds:
            r_out = "r" + str(i+1)
        else:
            r_out = None
        df = loopRounds(r_in,r_out,p_dict, df, 
                        tourn, court, all_rounds)
    
    #print(df)
    df.reset_index(drop=True,inplace=True)
    
    writer = pd.ExcelWriter(out_file)
    df.to_excel(writer,'Sheet1',header=True,index=True)
    writer.save()

#file_name = {'r1':['R Nadal', 'R Federer']}
#wrapper(file_name, type = 'dict', out_file = '_temp.xls',
#        tourn = 'US', court = 'H', all_rounds = False)