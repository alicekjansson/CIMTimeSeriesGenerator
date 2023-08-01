# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import aggregate
import PySimpleGUI as sg

#Create GUI
sg.theme('DarkTeal4')
layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
          [sg.Text('Choose dwelling:')],
          [sg.Combo(['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri'],key='TYP',enable_events=True,default_value='Småhus Direktel')],
          [sg.Text('Choose number of objects:')],
          [sg.Input('100',key='nbr_objects',size=(5, 1))],
          [sg.Text('Choose bidding area:')],
          [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4')],
          [sg.Text('Choose season:')],
          [sg.Combo(['Winter','Autumn/Spring','Summer'],key='SEASON',enable_events=True,default_value='Winter')],
          [sg.Text('Choose day:')],
          [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday')],
          [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name')],
          [sg.Text('CSV Location', size=(12, 1)), sg.Input('C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Generated_csv',key='loc'), sg.FolderBrowse()],
          [sg.Submit('Only Generate Timeseries'),sg.Submit('Generate and Save as CSV'),sg.Exit()]]

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

dwellings=['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri']
bids=['SE1','SE2','SE3','SE4']
seasons=['Winter','Autumn/Spring','Summer']
days=['Weekday','Weekend']

# Run GUI
while True:
    event, values = window.read()
    # End program if user closes window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if values['TYP']:
        choice=values['TYP']                # Get user choice
        for i,d in enumerate(dwellings):    # Get user choice in int form
            if choice == d:
                typ=i                       # Update house dwelling type
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
    if event == 'Only Generate Timeseries':
        #Add check for if not all categories are defined by user
        if not ( values['TYP'] and values['SEASON']and values['ZONE'] and values['DAY']):
            sg.popup('Not all user input defined')
        else:
            try:
                N=int(values['nbr_objects'])
                PtotS=aggregate(typ,elomr,arstid,dag,N)
                break
            except ValueError:
                sg.popup('Please enter integer nbr of objects')
    if event == 'Generate and Save as CSV':
        #Add check for if not all categories are defined by user
        if not ( values['TYP'] and values['SEASON']and values['ZONE'] and values['DAY']):
            sg.popup('Not all user input defined')
        elif not ( values['Name'] and values['loc']):
            sg.popup('CSV name or location not defined')
        else:
            try:
                N=int(values['nbr_objects'])
                PtotS=aggregate(typ,elomr,arstid,dag,N)
                name=values['Name']
                loc=values['loc']
                csv_loc=str(loc)+'/'+str(name)+'.csv'
                PtotS.to_csv(csv_loc)
                break
            except ValueError:
                sg.popup('Please enter integer nbr of objects')
            
            break

window.close()


# TO-DO:
# Add option to select yearly or daily profile
# Aggregate load profiles to higher voltage levels
# Add selection of voltage level / average power
# Deal with generation
# Add option to randomize load curves slightly?
