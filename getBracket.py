# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:22:04 2018

@author: edbras
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from unidecode import unidecode

"""
First format from first inital last name to first name last name
Requires typing every player's first name
Returns a DataFrame
"""

def fixName(df_r1, num_players):
    #df_r1["Full Name"]=""
    for index in range(0,num_players):
        player = df_r1["Name"][index]
        #print (player)
        name = input("Enter {0}'s First Name:".format(player))
        if unidecode(player.split(" ",1)[1]) == "Dere":
            new_name = name + " " + "Djere"
        else:
            new_name = name + " " + unidecode(player.split(" ",1)[1]).replace("-"," ")
        df_r1["Full Name"][index] = new_name.title()
        
    return df_r1

"""
Get US Open Draw from wikipedia
Note: Player format comes in as first initial last name

Use the num_players option for troubleshooting
If num_players is left blank, it'll loop all players

Returns a DataFrame
"""

def getBracket (new_bracket = True, num_players = 0):
    if new_bracket == True:
        url = "https://en.wikipedia.org/wiki/2018_US_Open_%E2%80%93_Men%27s_Singles#Draw"
        #print(url)
    
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()
    
        soup = soup.findAll('table')
        df = pd.DataFrame()   
        
        for i in range(4,12):
            #print(i)
            soup_i = soup[i]
            df1, = pd.read_html(str(soup_i))
            df1 = df1.iloc[1:,2]
            #print(df1)
            df = pd.concat([df,df1])
        
        if num_players == 0:
            num_players = int(df.count())

        df.reset_index(drop=True,inplace=True)
        df.columns= ["Name"]
        df["Full Name"] = "N/A"
        print(df)
        df = fixName(df,num_players)
        
        print(df)
        # Write to Excel to prevent having to type first names every time        
        writer = pd.ExcelWriter('bracket.xls')
        df.to_excel(writer,'Sheet1',header=True,index=True)
        writer.save()
        
    else:
        df = pd.read_excel("bracket.xls"
                      ,sheet_name="Sheet1"
                      ,header=0)
    
    return df
   # print(df)

#df = getBracket(new_bracket = True, num_players = 0)

#print(df)
