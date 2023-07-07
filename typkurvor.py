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
          [sg.Combo(['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri'])],
          [sg.Text('Choose bidding area:')],
          [sg.Combo(['SE1','SE2','SE3','SE4'])],
          [sg.Text('Choose season:')],
          [sg.Combo(['Winter','Autumn/Spring','Summer'])],
          [sg.Text('Choose day:')],
          [sg.Combo(['Weekday','Weekend'])],
          [sg.Submit('Generate Timeseries'),sg.Exit()]]

# Create the window
window = sg.Window('Timeseries Generator', layout)

# Make choices

# 0 Småhus direktel
# 1 Småhus hushållsel
# 2 Lägenhet
# 3 Industri
typ=0

# Välj elområde
elomr=2

# 0 Vinter
# 1 Vår/Höst
# 2 Sommar
arstid=2

# 0 Vardag
# 1 Helg och helgdag
dag=0

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
    for i,d in enumerate(dwellings):
        if event == d:
            typ=i
    for i,d in enumerate(bids):
        if event == d:
            elomr=i+1
    for i,d in enumerate(seasons):
        if event == d:
            arstid=i
    for i,d in enumerate(days):
        if event == d:
            dag=i
    if event == 'Generate Timeseries':
        P=generate_timeseries(typ,elomr,arstid,dag)
        break

window.close()


# TO-DO:
# Make selections in GUI change values in script
# Add to GUI that P is saved as csv 
# Add option to select yearly or daily profile
# Deal with industry load
# Aggregate load profiles to higher voltage levels
# Add selection of voltage level / average power
# Deal with generation
