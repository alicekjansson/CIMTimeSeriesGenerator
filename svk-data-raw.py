# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:28:19 2023

@author: Alice
"""

import pandas as pd

#Import data sources and pick relevant data
def import_data(name):
    df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SVK-Data/timvarden-%s-01-12.csv' %name,sep=';')
    df=df.iloc[4:,:]
    df=df.dropna(how='all')
    df=df.dropna(how='all',axis=1)
    df=df.rename(columns={' ':'Timestamp'})
    df=df[['Timestamp','Timmätt förbr','Timmätt förbr.1','Timmätt förbr.2','Timmätt förbr.3']]
    df=df.rename(columns={'Timmätt förbr':'Forb SE1','Timmätt förbr.1':'Forb SE2','Timmätt förbr.2':'Forb SE3','Timmätt förbr.3':'Forb SE4'})
    return df

#Add dataframes together and make sure the format is right
years=['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
dfs=[]
for year in years:
    dfs.append(import_data(year))
all_years=pd.concat(dfs,ignore_index=True)
all_years['Forb SE1']=[el.replace(' ','') for el in all_years['Forb SE1']]
all_years['Forb SE2']=[el.replace(' ','') for el in all_years['Forb SE2']]
all_years['Forb SE3']=[el.replace(' ','') for el in all_years['Forb SE3']]
all_years['Forb SE4']=[el.replace(' ','') for el in all_years['Forb SE4']]
all_years.index=all_years['Timestamp']
all_years=all_years.drop('Timestamp',axis=1)
all_years=all_years.astype(float)

#Divide into dates, times, etc
for i,el in all_years.transpose().items():
    temp=i.split(' ')
    all_years.loc[i,'Dateyear']=temp[0]
    all_years.loc[i,'Time']=temp[1]
    temp=temp[0].split('.')
    all_years.loc[i,'Date']=str(temp[1]+'.'+temp[0])
    all_years.loc[i,'Month']=temp[1]
    all_years.loc[i,'Year']=temp[2]
#%%
