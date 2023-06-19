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

year=df.groupby('Timedate').agg('mean')
yearmax=df.groupby('Timedate').agg('max')
yearmin=df.groupby('Timedate').agg('min')
# fig,ax=plt.subplots(1,figsize=[8,5])
# year['Forb'].plot(ax=ax,label='Mean')
# yearmax['Forb'].plot(ax=ax,label='Max')
# yearmin['Forb'].plot(ax=ax,label='Min')
# ax.set_ylabel('Consumption [MW]')
# plt.xticks(rotation=90)
# plt.legend()

df['Daytime']=df['Weekday']+df['Time']
day=df.groupby('Daytime').agg('mean')
daymax=df.groupby('Daytime').agg('max')
daymin=df.groupby('Daytime').agg('min')
fig,ax=plt.subplots(1,figsize=[8,5])
day['Forb'].plot(ax=ax,label='Mean')
daymax['Forb'].plot(ax=ax,label='Max')
daymin['Forb'].plot(ax=ax,label='Min')
ax.set_ylabel('Consumption [MW]')
plt.xticks(rotation=90)
plt.legend()


weekly_profile=pd.DataFrame({'Max':daymax['Forb'],'Mean':day['Forb'],'Min':daymin['Forb']})
yearly_profile=pd.DataFrame({'Max':yearmax['Forb'],'Mean':year['Forb'],'Min':yearmin['Forb']})

weekly_profile.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\weekly_profile_load_se4.csv')
yearly_profile.to_csv(r'C:\Users\Alice\OneDrive - Lund University\Dokument\GitHub\CIMProject\yearly_profile_load_se4.csv')