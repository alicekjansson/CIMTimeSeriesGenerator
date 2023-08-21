# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
from alice_func import aggregate
import PySimpleGUI as sg

# Check themes
#sg.theme_previewer()

sg.theme('LightGreen5')
col1 = [
    [sg.Text('Choose bidding area:')],  
    [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4',size=(10, 1))],  
]
col2 = [
    [sg.Text('Choose day:')],
    [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday',size=(10, 1))],  
]
col3 = [
    [sg.Text('Choose season:')],
    [sg.Combo(['Winter','Autumn/Spring','Summer'],key='SEASON',enable_events=True,default_value='Winter',size=(10, 1))], 
]

loads=[1,2,3,4]
load_left = [
    [sg.Text("Loads")],
    [sg.Listbox(loads,key='LOADS',size=[100,50],enable_events=True)],
]
r1=sg.Radio('Average','load',default=True,enable_events=True,key='AVERAGE')
r2=sg.Radio('Urban area','load',enable_events=True,key='URBAN')
r3=sg.Radio('Rural area','load',enable_events=True,key='RURAL')
r4=sg.Radio('Industrial area','load',enable_events=True,key='INDUSTRY')
load_right = [
    [sg.Text("Select load case")],
    [r1],
    [r2],
    [r3],
    [r4]
]

layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
          [sg.HorizontalSeparator()],
          [sg.Column(col1,size=[150,50]),
           sg.Column(col2,size=[150,50]),
           sg.Column(col3,size=[150,50])],
          [sg.HorizontalSeparator()],
          [sg.Column(load_left,size=[200,150]),
           sg.VerticalSeparator(),
           sg.Column(load_right,size=[200,150])],
          [sg.HorizontalSeparator()],
          [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name')],
          [sg.Text('CSV Location', size=(12, 1)), sg.Input('./Generated_csv',key='loc'), sg.FolderBrowse()],
          [sg.Submit('Only Generate Timeseries'),sg.Submit('Generate and Save as CSV'),sg.Exit()]
          ]

# Create the window
window = sg.Window('Load Timeseries Generator', layout)

types=['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri']
bids=['SE1','SE2','SE3','SE4']
seasons=['Winter','Autumn/Spring','Summer']
days=['Weekday','Weekend']


# Run GUI
while True:
    P_scale=200   #NEED TO SCALE
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if values['ZONE']:
        choice=values['ZONE']                # Get user choice
        for i,d in enumerate(bids):
            if choice == d:
                elomr=i+1
    if values['SEASON']:
        choice=values['SEASON']                # Get user choice
        for i,d in enumerate(seasons):
            if choice == d:
                arstid=i
    if values['DAY']:
        choice=values['DAY']                # Get user choice
        for i,d in enumerate(days):
            if choice == d:
                dag=i
    if values['AVERAGE']==True:
        dwellings=[0.94,0.03,0.03]
    if values['URBAN']==True:
        dwellings=[0.69,0.30,0.01]
    if values['RURAL']==True:
        dwellings=[0.96,0.01,0.03]
    if values['INDUSTRY']==True:
        dwellings=[0.88,0.02,0.10]
    for n,gen in enumerate(['Only Generate Timeseries','Generate and Save as CSV']):
        if event == gen:
            P_tot=[]
            for i,nbr in enumerate(dwellings):
                typ=i
                N=int(nbr*P_scale)
                P_tot.append(aggregate(typ,elomr,arstid,dag,N))
            P_tot=pd.DataFrame(P_tot).sum()
            fig,ax=plt.subplots(1,figsize=[8,4])
            P_tot.plot(ax=ax)
            ax.set_xlabel('Hour')
            ax.set_ylabel('Total consumption (kW)')
            dwellings=['Småhus','Lägenhet','Industri']
            ax.set_title('Aggregated load')
            if n==0:
                window.close()
            if n == 1:
                if not ( values['Name'] and values['loc']):
                    sg.popup('CSV name or location not defined')
                else:
                    name=values['Name']
                    loc=values['loc']
                    csv_loc=str(loc)+'/'+str(name)+'.csv'
                    P_tot.to_csv(csv_loc)
                    window.close()
            
            
window.close()        

