# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:20:54 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg

# Import data for SE4
df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SVK-Data/all_years.csv',sep=',').iloc[:,1:]

# Aggregate based on defined time = hour and cat = generation category
def aggregate(df,time,cat):
    year=df.groupby(time).agg('mean')
    yearstd=df.groupby(time).agg('std')
    yearly_profile=pd.DataFrame()
    for col in [el for el in df.columns if cat in el]:
        yearly_profile[col] = year[col]
        yearly_profile[str(col) +' Upper'] = year[col]+yearstd[col]
        yearly_profile[str(col) +' Lower'] = year[col]-yearstd[col]
    return yearly_profile

# Plot generation type of all bidding areas
def plot(profile,title):
    fig,ax=plt.subplots(1,figsize=[8,4])
    profile=profile.iloc[:,::3]
    profile.plot(ax=ax)
    ax.set_ylabel('Consumption [MW]')
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.legend()

# Plot average, average +- std of one generation type in one bidding area
def plot_single(profile,se,title):
    fig,ax=plt.subplots(1,figsize=[8,4])
    profile[str(se) + ' Upper'].plot(ax=ax,label='Upper')
    profile[str(se)].plot(ax=ax,label='Mean')
    profile[str(se) + ' Lower'].plot(ax=ax,label='Lower')
    ax.set_ylabel('Consumption [MW]')
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.legend()
    
def weekday(df):
    return df[(df['Weekday']!=5) & (df['Weekday'] != 6)]

def weekend(df):
    return df[(df['Weekday']==5) | (df['Weekday'] == 6)]

hydro=aggregate(df,'Hour','Hydro')
plot_single(hydro,'Hydro SE4','Hydro SE4')
plot(hydro,'Hydro')