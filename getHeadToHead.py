# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:22:04 2018

@author: edbras

Definition: getH2H function pulls head to head results
Returns: df with head-to-head
"""

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

def getH2H (player1,player2):
    url = "http://www.ultimatetennisstatistics.com/headToHead?name1={0}&name2={1}".format(player1,player2)
    print(url)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    found = False
    while found == False:
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        browser.close()
        #print(soup.find("table"))
        if soup.find("table") != None:
            found = True
    #print(soup)

    soup = soup.findAll("table")[0]
    
    #print(soup)
    
    df1, = pd.read_html(str(soup))
    #print(df1)
    df1 = df1.iloc[0:34,[0,2,4]]
    #print(df1)
    #print(df1.columns)
    names = [df1.columns[0][0], 'vs',df1.columns[2][0]]
    h2h = [df1.columns[0][1], df1.columns[2][1]]
    df1.columns = names
    #print(df1.columns)
    #print(df1)
    #df1[[0,1,2]] = df1[[1,0,2]]
    #df1.reset_index()
    df1.set_index("vs", drop=True, inplace=True)
   # print(df1.index)
    if "H2H" in df1.index:
      #  print(True)
        df1.drop("H2H", inplace=True)
   # print(df1)
   # print(h2h)    
    df1.loc["H2H"] = h2h
   # print(df1)
    return df1

"""
Sample call

player1 = "Denis%20Kudla".replace(" ","%20")
player2 = "Malek%20Jaziri".replace(" ","%20")

df_h2h = getH2H(player1,player2)
print(df_h2h)

print(df_h2h.loc["H2H"][0])
print(df_h2h.loc["H2H"][1])

"""

#soup_player = soup.findAll("tr")[0]
#soup_h2h = soup.findAll("tr")[1]
#print(soup_player)
#print(soup_h2h)