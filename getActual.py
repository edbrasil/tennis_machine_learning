# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:18:33 2018

@author: edbras
"""
"""
Get actual results of a given tournament
Specified by url_use and out_file variables
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import json

url_use = "https://en.wikipedia.org/wiki/2019_Australian_Open_%E2%80%93_Men%27s_Singles#Draw"
out_file = "R1_A2019.json"
all_rounds = False
col_list = [2, 11, 12, 13, 2, 3, 4]
t_start = [5, 4, 4, 4, 3, 3, 3 ]
t_end = [13, 12, 12, 12, 4, 4, 4]

#col_list = [2, 3, 4]
#t_start = [3, 3, 3]
#t_end = [4, 4, 4]
"""
getBracket returns a DataFrame with players for
a given round

column, t_start, t_end specify given parameters
based on the Wikipedia page
"""

def getBracket (new_bracket = True, column = 11, 
                t_start = 4, t_end = 12):
    if new_bracket == True:
        url = url_use
        #print(url)
    
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()
    
        soup = soup.findAll('table')
        df = pd.DataFrame()   
        
        for i in range(t_start, t_end):
            soup_i = soup[i]
            df1, = pd.read_html(str(soup_i))
            
            #print(df1)
            if column == 12 or column == 13:
                df1.iloc[8,13] = df1.iloc[8,12]
                df1.iloc[8,12] = ""
#            
            if t_start == 3:
                df1.iloc[13,3] = df1.iloc[13,4]
                df1.iloc[13,4] = ""
                df1.iloc[5,3] = df1.iloc[5,4]
                df1.iloc[5,4] = ""
                df1.iloc[8,4] = df1.iloc[8,3]
                df1.iloc[8,3] = ""
                
#            if t_start == 3:
#                writer = pd.ExcelWriter('temp.xls')
#                df1.to_excel(writer,'Sheet1',header=True,index=True)
#                writer.save()
#                
#                wait = input("Waiting:")
#                if wait == "Y":
#                    continue
               
                #df1 = pd.read_excel("temp.xls", sheet_name="Sheet1", header=0)

            df1 = df1.iloc[1:,column]

            df1.dropna(inplace=True)
            #print (~df1.str.contains(r'[0-9]'))
            df1 = df1.loc[~df1.str.contains(r'[0-9]')]
            df1 = df1[~df1.isin(["","WC","LL","Q","PR","w/o"])]
#            df1 = df1[df1 != "WC"]
#            df1 = df1[df1 != "LL"]
#            df1 = df1[df1 != "Q"]
#            df1 = df1[df1 != "PR"]
            #print(df1)

            df = pd.concat([df,df1])
        
#        if num_players == 0:
#            num_players = int(df.count())

        df.reset_index(drop=True,inplace=True)
        df.columns= ["Name"]
    
    return df

"""
Use getBracket to get round results
"""

def getCorrectRound(col = 11, r_name = "round2", t_s = 4, t_e=12):
    df = getBracket(new_bracket = True, 
                    column = col, t_start = t_s, t_end = t_e)
    #df.to_json("C_" + r_name.replace(" ","") + ".json",orient="values")
    
    return df

"""
Separate function to get champion since format is
different in Wikipedia page
"""

def getChampion():
    url = url_use
    #print(url)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "lxml")
    browser.close()

    soup = soup.findAll('table')[0].findAll('a')[2].text
    df1 = pd.DataFrame([str(soup)])
    
    df1.columns = ["Name"]
    
    return df1


"""
1.Use functions to get round-by-round
2.Add to a dictionary
3.Output to JSON
"""
df1 = getCorrectRound(col=col_list[0],r_name = "round1",
                          t_s=t_start[0],t_e=t_end[0])
if all_rounds:
    df2 = getCorrectRound(col=col_list[1],r_name = "round2",
                          t_s=t_start[1],t_e=t_end[1])
    df3 = getCorrectRound(col=col_list[2],r_name = "round3",
                          t_s=t_start[2],t_e=t_end[2])
    df4 = getCorrectRound(col=col_list[3],r_name = "round4",
                          t_s=t_start[3],t_e=t_end[3])
    df5 = getCorrectRound(col=col_list[4],r_name = "quarterfinal",
                          t_s=t_start[4],t_e=t_end[4])
    df6 = getCorrectRound(col=col_list[5],r_name = "semifinal",
                          t_s=t_start[5],t_e=t_end[5])
    df7 = getCorrectRound(col=col_list[6],r_name = "final",
                          t_s=t_start[6],t_e=t_end[6])
    df8 = getChampion()

if all_rounds:
    dict = {"Round 1": df1.values.tolist(),
        "Round 2" : df2.values.tolist(),
        "Round 3" : df3.values.tolist(),
        "Round 4" : df4.values.tolist(),
        "Quarterfinal" : df5.values.tolist(),
        "Semifinal" : df6.values.tolist(),
        "Final" : df7.values.tolist(),
        "Winner" : df8.values.tolist()}
else:
    dict = {"Round 1": df1.values.tolist()}

with open(out_file, 'w') as fp:
    json.dump(dict, fp)

