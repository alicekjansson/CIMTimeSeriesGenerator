# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:01:20 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import aggregate

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

dwellings=['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri']
bids=['SE1','SE2','SE3','SE4']
seasons=['Winter','Autumn/Spring','Summer']
days=['Weekday','Weekend']

andel_elvarme=0.3   #Cirka 30% av småhus uppvärmda med elvärme enligt Energimyndighetens statistik 2021

#Sammanlagringsfaktor
S=[0.81,0.59,0.6,0.76]
#Antal objekt
N=100


#Create timeseries
typ=0
elomr=4
arstid=0
dag=1


PtotS=aggregate(typ,elomr,arstid,dag,N)