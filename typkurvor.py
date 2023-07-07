# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import forb,tempberoende,graddagar,load_df, choose_curve, choose_temp

# Make choices

# 0 Småhus direktel
# 1 Småhus hushållsel
# 2 Lägenhet
# 3 Industri
typ=1

# Välj elområde
elomr=4

# 0 Vinter
# 1 Vår/Höst
# 2 Sommar
arstid=1

# 0 Vardag
# 1 Helg och helgdag
dag=0

#Medelårsförbrukning kWh
medelforb=forb()

# Temperaturberoende
psi=tempberoende()

# Graddagar, SE1-SE4
graddag=graddagar()

# Calculate normalized annual energy and average load

Ean=medelforb[typ-1]/(1+psi[typ]*((graddag[elomr-1])/3978)-1)
Pav=Ean/8760

# Import standard load curves
# För småhus är vanligaste uppvärmningssätt el, antingen direktverkande eller luftvärmepump. Även endast hushållsel tittas på (t.ex. fjärrvärme)
df=load_df()

#Define seasonal temperatures in se1-se4
temperatur=pd.DataFrame(index=['Vinter','Höst/Vår','Sommar'],columns=['se1','se2','se3','se4'])
temperatur['se1']=[-20,0,10]
temperatur['se2']=[-20,0,15]
temperatur['se3']=[-10,5,20]
temperatur['se4']=[-5,10,20]

# Select correct load curve and temperatures
load_curve=choose_curve(df,typ,elomr,arstid,dag)
temp=temperatur.iloc[arstid,elomr-1]
load_temps=choose_temp(load_curve,temp,arstid,elomr)
load_curve=load_curve.iloc[:,load_temps[1]]

#Transform load curve
P=pd.DataFrame(index=load_curve.index,columns=['P'])

for i,row in load_curve.transpose().items():
    pnew=(row.iloc[1]-row.iloc[0])/(load_temps[0][1]-load_temps[0][0])*(temp-load_temps[0][0])
    P.loc[i,'P']=float(pnew)*Pav

fig,ax=plt.subplots(1,figsize=[8,4])
P.plot(ax=ax)
load_curve.plot(ax=ax)
ax.set_ylabel('Consumption [kW]')
ax.set_title('Load curve')
plt.xticks(rotation=45)
plt.legend()