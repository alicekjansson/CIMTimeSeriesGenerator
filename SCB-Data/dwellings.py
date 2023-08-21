# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 10:43:25 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SCB-Data/dwellings.csv')
df.index=df['region']
df=df.iloc[:,2:]
df['totalt1']=df['bostad']+df['industri']
df['Andel bostad']=df['bostad']/df['totalt1']
df['Andel industri']=df['industri']/df['totalt1']
medel=df.mean()

df2=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SCB-Data/houses.csv')
df2.index=df2['region']
df2=df2.iloc[:,2:]

df2['småhus']=df2['småhus friliggande']+df2['småhus kedjehus']+df2['småhus flera lägenheter']+df2['småhus radhus']
df2['totalt']=df2['småhus']+df2['flerbostadshus']
houses_medel=df2.mean()