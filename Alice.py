# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 08:36:09 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt

#Data for SE4
df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/Doktorand IEA/ACTUAL/Data/SVK SE4/timvarden_allyears_SE4_edit.csv',sep=',')
df=df[df['Year'] != 2022]
df=df.iloc[:,2:]
df['Daytime']=df['Weekday']+df['Time']

def aggregate(df,time,col):
    year=df.groupby(time).agg('mean')
    yearmax=df.groupby(time).agg('max')
    yearmin=df.groupby(time).agg('min')
    yearly_profile=pd.DataFrame({'Max':yearmax[col],'Mean':year[col],'Min':yearmin[col]})
    return yearly_profile

def plot(profile,title):
    fig,ax=plt.subplots(1,figsize=[8,4])
    profile['Max'].plot(ax=ax,label='Max')
    profile['Min'].plot(ax=ax,label='Min')
    profile['Mean'].plot(ax=ax,label='Mean')
    ax.set_ylabel('Consumption [MW]')
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.legend()

year=aggregate(df,'Timedate','Forb')
week=aggregate(df,'Daytime','Forb')

weekdays=df[(df['Weekday']!='Saturday') & (df['Weekday'] != 'Sunday')]
weekends=df[(df['Weekday']=='Saturday') | (df['Weekday'] == 'Sunday')]
wday=aggregate(weekdays,'Time','Forb')
wend=aggregate(weekends,'Time','Forb')

#%%

plot(year,'Yearly profile')
plot(week,'Weekly profile')
plot(wday, 'Daily profile, weekday')
plot(wend, 'Daily profile, weekend')

#Save to csv files
# week.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\weekly_profile_load_se4.csv')
# year.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\yearly_profile_load_se4.csv')
# wday.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\weekday_profile_load_se4.csv')
# wend.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\weekend_profile_load_se4.csv')