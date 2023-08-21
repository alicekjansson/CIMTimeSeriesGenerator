# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:20:54 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from scipy.stats import norm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import data for SE4
df=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/SVK-Data/all_years.csv',sep=',').iloc[:,1:]

# Aggregate based on defined time = hour and cat = generation category
def aggregate(df,time,cat,scale):
    year=df.groupby(time).agg('mean')
    yearly_profile=pd.DataFrame()
    original_scale=year[cat].max()
    scaling=scale/original_scale
    yearly_profile[cat] = [el*scaling for el in year[cat]]
    yearstd=(df[cat]*scaling).std()
    variation=norm.rvs(0,yearstd,size=1)[0]
    yearly_profile[str(cat) +' Upper'] = yearly_profile[cat]+yearstd
    yearly_profile[str(cat) +' Lower'] = yearly_profile[cat]-yearstd
    yearly_profile[str(cat) +' Selected'] = yearly_profile[cat]+variation
    return yearly_profile

# Plot average, average +- std of one generation type in one bidding area
def plot(profile,se,title):
    fig,ax=plt.subplots(1,figsize=[8,4])
    profile[str(se) + ' Upper'].plot(ax=ax,label='Upper')
    profile[str(se)].plot(ax=ax,label='Mean')
    profile[str(se) + ' Lower'].plot(ax=ax,label='Lower')
    profile[str(se) + ' Selected'].plot(ax=ax,label='Selection')
    ax.set_ylabel('Consumption [MW]')
    ax.set_title(title)
    plt.xticks(rotation=45)
    plt.legend()
    
def weekday(df):
    return df[(df['Weekday']!=5) & (df['Weekday'] != 6)]

def weekend(df):
    return df[(df['Weekday']==5) | (df['Weekday'] == 6)]

sg.theme('LightGreen5')
bids=['SE1','SE2','SE3','SE4']
days=['Weekday','Weekend']

layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
          [sg.Text('Choose generation type:')],
          [sg.Combo(['Hydro','Wind','PV','CHP','Nuclear'],key='GEN',enable_events=True,default_value='Hydro')],
          [sg.Text('Choose unit size:')],
          [sg.Input('5',key='SIZE',size=[10,10]),sg.Text('MW')],
          [sg.Text('Choose bidding area:')],  
          [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4',size=[10,10])],
          [sg.Text('Choose day:')],
          [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday')],
          [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name')],
          [sg.Text('CSV Location', size=(12, 1)), sg.Input('./Generated_csv',key='loc'), sg.FolderBrowse()],
          [sg.Submit('Only Generate Timeseries'),sg.Submit('Generate and Save as CSV'),sg.Exit()]
          ]

# Create the window
window = sg.Window('Load Timeseries Generator', layout)

# Run GUI
while True:
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if values['ZONE']:
        zone=values['ZONE']                # Get user choice
    if values['DAY']:
        choice=values['DAY']                # Get user choice
        for i,d in enumerate(days):
            if choice == d:
                dag=i
    if values['GEN']:
        gen=values['GEN']                # Get user choice
    for n,ev in enumerate(['Only Generate Timeseries','Generate and Save as CSV']):
        if event == ev:
            if (gen == 'Nuclear') and (zone != 'SE3'):
                sg.popup('Nuclear power exists only in SE3')
                break
            try:
                size=float(values['SIZE'])
                profile=aggregate(df,'Hour',str(gen + ' ' +zone),size)
                plot(profile,str(gen + ' ' +zone),str(gen + ' ' +zone))
            except ValueError:
                sg.popup('Please enter valid size of generating unit')
                break
            if n==0:    #Only show time series
                window.close()
            if n == 1:  #Show and save as csv
                if not ( values['Name'] and values['loc']):
                    sg.popup('CSV name or location not defined')
                else:
                    name=values['Name']
                    loc=values['loc']
                    csv_loc=str(loc)+'/'+str(name)+'.csv'
                    profile[str(gen + ' ' +zone+ ' Selected')].to_csv(csv_loc)
                    window.close()
window.close()        
