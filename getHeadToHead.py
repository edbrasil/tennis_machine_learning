# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 16:22:04 2018

@author: edbras
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
    df1 = df1.iloc[0:34,0:3]
    df1[[0,1,2]] = df1[[1,0,2]]
    df1.set_index(0, drop=True, inplace=True)
   # print(df1)
    return df1

"""
Sample call

player1 = "Novak Djokovic".replace(" ","%20")
player2 = "Juan Martin Del Potro".replace(" ","%20")

df_h2h = getH2H(player1,player2)
#print(df_h2h)

print(df_h2h.loc["H2H"][1])
print(df_h2h.loc["H2H"][2])
"""


#soup_player = soup.findAll("tr")[0]
#soup_h2h = soup.findAll("tr")[1]
#print(soup_player)
#print(soup_h2h)