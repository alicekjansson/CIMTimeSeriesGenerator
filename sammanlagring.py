# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 11:01:20 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import generate_timeseries, load_df, forb, graddagar, tempberoende, choose_curve, choose_temp, transform_load

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

#Sammanlagringsfaktor
S=[0.81,0.59,0.6,0.76]
#Antal objekt
N=100


#Create timeseries
typ=0
elomr=4
arstid=0
dag=1

def aggregate(typ,elomr,arstid,dag):
    Pall=pd.DataFrame()
    for i in range(N):
        P=generate_timeseries(typ,elomr,arstid,dag,False)
        Pall[i]=P
    Ptot=Pall.sum(axis=1)
    PtotS=Ptot*S[typ]
    fig,ax=plt.subplots(1,figsize=[8,4])
    PtotS.plot(ax=ax)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Total consumption (kW)')
    ax.set_title('Aggregated load of ' + str(N) + ' x ' + str(dwellings[typ]))
    return PtotS

PtotS=aggregate(typ,elomr,arstid,dag)