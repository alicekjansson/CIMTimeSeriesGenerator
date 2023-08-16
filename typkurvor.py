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
# sg.theme_previewer()

sg.theme('LightGreen5')
layout1 = [
    [sg.Text("#Houses:")],
    [sg.Input('100',key='nbr_house')],
    [sg.Text('Choose bidding area:')],  
    [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4',size=[10,10])],
]
layout2 = [
    [sg.Text("#Apartment buildings:")],
    [sg.Input('10',key='nbr_apartm')],
    [sg.Text('Choose season:')],
    [sg.Combo(['Winter','Autumn/Spring','Summer'],key='SEASON',enable_events=True,default_value='Winter')],
]
layout3 = [
    [sg.Text("#Industry:")],
    [sg.Input('10',key='nbr_industry')],
    [sg.Text('Choose day:')],
    [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday')],
]

layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
          [sg.Text('Choose dwellings:')],
          [sg.Column(layout1,size=[150,150]),
           sg.Column(layout2,size=[150,150]),
           sg.Column(layout3,size=[150,150]),],
          [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name')],
          [sg.Text('CSV Location', size=(12, 1)), sg.Input('./Generated_csv',key='loc'), sg.FolderBrowse()],
          [sg.Submit('Only Generate Timeseries'),sg.Submit('Generate and Save as CSV'),sg.Exit()]
          ]

# Create the window
window = sg.Window('Load Timeseries Generator', layout)

# TYP
# 0 Småhus direktel
# 1 Småhus hushållsel
# 2 Lägenhet
# 3 Industri
# SEASON
# 0 Vinter
# 1 Vår/Höst
# 2 Sommar
# DAY
# 0 Vardag
# 1 Helg och helgdag

dwellings=['Småhus','Lägenhet','Industri']
types=['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri']
bids=['SE1','SE2','SE3','SE4']
seasons=['Winter','Autumn/Spring','Summer']
days=['Weekday','Weekend']


# Run GUI
while True:
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # if values['TYP']:
    #     choice=values['TYP']                # Get user choice
    #     for i,d in enumerate(dwellings):    # Get user choice in int form
    #         if choice == d:
    #             typ=i                       # Update house dwelling type
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
    for n,gen in enumerate(['Only Generate Timeseries','Generate and Save as CSV']):
        if event == gen:
            P_tot=[]
            for i,nbr in enumerate(['nbr_house','nbr_apartm','nbr_industry']):
                typ=i
                #Add check for if not all categories are defined by user
                if not ( values['SEASON']and values['ZONE'] and values['DAY']):
                    sg.popup('Not all user input defined')
                else:
                    try:
                        N=int(values[nbr])
                        P_tot.append(aggregate(typ,elomr,arstid,dag,N))
                    except ValueError:
                        sg.popup('Please enter integer nbr of objects')
                        break
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

