# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alice_func import generate_timeseries
import PySimpleGUI as sg

#Create GUI
sg.theme('DarkTeal4')
layout = [[sg.Text('Define the requirements of time series')],
          [sg.Text('Choose dwelling:')],
          [sg.Combo(['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri'],key='TYP',enable_events=True)],
          [sg.Text('Choose bidding area:')],
          [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True)],
          [sg.Text('Choose season:')],
          [sg.Combo(['Winter','Autumn/Spring','Summer'],key='SEASON',enable_events=True)],
          [sg.Text('Choose day:')],
          [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True)],
          [sg.Submit('Generate Timeseries'),sg.Exit()]]

# Create the window
window = sg.Window('Timeseries Generator', layout)

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

#OBS DETTA FUNKAR EJ MÅSTE LÖSA SÅ ATT MAN KAN DEFINIERA VÄRDENA I GUI
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
    if event == 'Generate Timeseries':
        P=generate_timeseries(typ,elomr,arstid,dag)
        break

window.close()


# TO-DO:
# Add to GUI that P is saved as csv 
# Add option to select yearly or daily profile
# Deal with industry load
# Aggregate load profiles to higher voltage levels
# Add selection of voltage level / average power
# Deal with generation
# Add option to randomize load curves slightly?
