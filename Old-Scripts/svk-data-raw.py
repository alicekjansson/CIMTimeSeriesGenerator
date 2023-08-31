# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 11:28:19 2023

@author: Alice
"""

import pandas as pd
from datetime import datetime

#Import data sources and pick relevant data
def import_data(name):
    df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SVK-Data/timvarden-%s-01-12.csv' %name,sep=';')
    df=df.iloc[4:,:]
    df=df.dropna(how='all')
    df=df.dropna(how='all',axis=1)
    df=df.rename(columns={' ':'Timestamp'})
    # df=df[['Timestamp','Timmätt förbr','Timmätt förbr.1','Timmätt förbr.2','Timmätt förbr.3']]
    df=df[['Timestamp','Timmätt förbr','Timmätt förbr.1','Timmätt förbr.2','Timmätt förbr.3',
           'Vattenkraft ','Vattenkraft .1','Vattenkraft .2','Vattenkraft .3',
           'Vindkraft','Vindkraft.1','Vindkraft.2','Vindkraft.3','Kärnkraft',
           'Värmekraft','Värmekraft.1','Värmekraft.2','Värmekraft.3',
           'Solkraft','Solkraft.1','Solkraft.2','Solkraft.3',]]
    df=df.rename(columns={'Timmätt förbr':'Load SE1','Timmätt förbr.1':'Load SE2','Timmätt förbr.2':'Load SE3','Timmätt förbr.3':'Load SE4'})
    df=df.rename(columns={'Vindkraft':'Wind SE1','Vindkraft.1':'Wind SE2','Vindkraft.2':'Wind SE3','Vindkraft.3':'Wind SE4'})
    df=df.rename(columns={'Solkraft':'PV SE1','Solkraft.1':'PV SE2','Solkraft.2':'PV SE3','Solkraft.3':'PV SE4'})
    df=df.rename(columns={'Värmekraft':'CHP SE1','Värmekraft.1':'CHP SE2','Värmekraft.2':'CHP SE3','Värmekraft.3':'CHP SE4'})
    df=df.rename(columns={'Vattenkraft ':'Hydro SE1','Vattenkraft .1':'Hydro SE2','Vattenkraft .2':'Hydro SE3','Vattenkraft .3':'Hydro SE4'})
    df=df.rename(columns={'Kärnkraft':'Nuclear SE3'})
    return df

#Add dataframes together and make sure the format is right
years=['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']
dfs=[]
for year in years:
    dfs.append(import_data(year))
all_years=pd.concat(dfs,ignore_index=True)

#%%
all_years['Load SE1']=[el.replace(' ','') for el in all_years['Load SE1']]
all_years['Load SE2']=[el.replace(' ','') for el in all_years['Load SE2']]
all_years['Load SE3']=[el.replace(' ','') for el in all_years['Load SE3']]
all_years['Load SE4']=[el.replace(' ','') for el in all_years['Load SE4']]
# all_years.index=all_years['Timestamp']
# all_years=all_years.drop('Timestamp',axis=1)
# all_years=all_years.astype(float)


# #Divide into dates, times, etc
# for i,el in all_years.transpose().items():
#     temp=i.split(' ')
#     all_years.loc[i,'Dateyear']=temp[0]
#     all_years.loc[i,'Time']=temp[1]
#     temp=temp[0].split('.')
#     all_years.loc[i,'Date']=str(temp[1]+'.'+temp[0])
#     all_years.loc[i,'Month']=temp[1]
#     all_years.loc[i,'Year']=temp[2]

#%%
df=all_years.copy()
df['Timestamp']=pd.to_datetime(df['Timestamp'])
df['Year']=[el.date().year for el in df['Timestamp']]
df['Hour']=[el.time().hour for el in df['Timestamp']]
df['Weekday']=[el.date().weekday() for el in df['Timestamp']]
df.to_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SVK-Data/all_years.csv')
