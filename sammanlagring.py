# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:01:20 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import generate_timeseries, load_df

# TYP
# 0 Småhus direktel
# 1 Småhus hushållsel
# 2 Lägenhet
# 3 Industri
# SEASON
# 0 Vinter
# 1 Vår/Höst
# 2 Sommar
# DAY
# 0 Vardag
# 1 Helg och helgdag

#Create timeseries
typ=3
elomr=4
arstid=0
dag=0
P=generate_timeseries(typ,elomr,arstid,dag)

#Sammanlagringsfaktor
S=[0.81,0.59,0.6,0.76]
#Antal objekt
N=100

df,std=load_df()