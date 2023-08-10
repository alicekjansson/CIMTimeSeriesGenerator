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

# Plot average, average +- std of one generation type in one bidding area
def plot(profile,se,title):
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

sg.theme('LightGreen5')
bids=['SE1','SE2','SE3','SE4']
days=['Weekday','Weekend']

layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
          [sg.Text('Choose generation type:')],
          [sg.Combo(['Hydro','Wind','PV','CHP','Nuclear'],key='GEN',enable_events=True,default_value='Hydro')],
          [sg.Text('Choose bidding area:')],  
          [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4',size=[10,10])],
          [sg.Text('Choose day:')],
          [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday')],
          [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name')],
          [sg.Text('CSV Location', size=(12, 1)), sg.Input('C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Generated_csv',key='loc'), sg.FolderBrowse()],
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
            profile=aggregate(df,'Hour',gen)
            plot(profile,str(gen + ' ' +zone),str(gen + ' ' +zone))
            if n==0:
                window.close()
            if n == 1:
                if not ( values['Name'] and values['loc']):
                    sg.popup('CSV name or location not defined')
                else:
                    name=values['Name']
                    loc=values['loc']
                    csv_loc=str(loc)+'/'+str(name)+'.csv'
                    profile[str(gen + ' ' +zone)].to_csv(csv_loc)
                    window.close()
window.close()        


# hydro=aggregate(df,'Hour','Hydro')
# plot_single(hydro,'Hydro SE4','Hydro SE4')
# plot(hydro,'Hydro')