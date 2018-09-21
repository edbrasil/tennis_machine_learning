# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:18:33 2018

@author: edbras
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def getBracket (new_bracket = True, num_players = 0, column = 11, 
                t_start = 4, t_end = 12):
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
        
        for i in range(t_start, t_end):
            #print(i)
            soup_i = soup[i]
            df1, = pd.read_html(str(soup_i))
            #print(df1)
            if column == 12 or column == 13:
                df1.iloc[8,13] = df1.iloc[8,12]
                df1.iloc[8,12] = ""
            
            if t_start == 3:
                df1.iloc[13,3] = df1.iloc[13,4]
                df1.iloc[13,4] = ""
            
#            writer = pd.ExcelWriter('temp.xls')
#            df1.to_excel(writer,'Sheet1',header=True,index=True)
#            writer.save()
#            
#            wait = input("Waiting:")
##            if wait == "Y":
##                continue
#            
#            df1 = pd.read_excel("temp.xls"
#                      ,sheet_name="Sheet1"
#                      ,header=0)
            df1 = df1.iloc[1:,column]

            df1.dropna(inplace=True)
            #print (~df1.str.contains(r'[0-9]'))
            df1 = df1.loc[~df1.str.contains(r'[0-9]')]
            df1 = df1[df1 != "WC"]
            #print(df1)

            df = pd.concat([df,df1])
        
        if num_players == 0:
            num_players = int(df.count())

        df.reset_index(drop=True,inplace=True)
        df.columns= ["Name"]
    
    return df

def getCorrectRound(col = 11, r_name = "round2", t_s = 4, t_e=12):
    df = getBracket(new_bracket = True, num_players = 0,
                    column = col, t_start = t_s, t_end = t_e)
    df.to_json("C_" + r_name.replace(" ","") + ".json",orient="values")

#getCorrectRound(col=11,r_name = "round2")
#getCorrectRound(col= 12, r_name = "round3")
#getCorrectRound(col=13, r_name = "round4")
getCorrectRound(col = 2,r_name = "quarterfinal", t_s =3, t_e=4)
getCorrectRound(col = 3,r_name = "semifinal", t_s =3, t_e=4)
getCorrectRound(col = 4,r_name = "final", t_s=3, t_e=4)
#print(df)
