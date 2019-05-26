# -*- coding: utf-8 -*-
"""
Created on Sun May 26 10:53:06 2019

@author: edbras
"""
import json

out_dict = {
        "Round 2" : [[""]]*64,
        "Round 3" : [[""]]*32,
        "Round 4" : [[""]]*16,
        "Quarterfinal" : [[""]]*8,
        "Semifinal" : [[""]]*4,
        "Final" : [[""]]*2,
        "Winner" : [[""]]
        }

with open('C_picks.json', 'w') as fp:
    json.dump(out_dict, fp)