# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 08:32:56 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
from alice_func import aggregate
import PySimpleGUI as sg

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
r1=sg.Radio('Average','load',default=True,enable_events=True)
r2=sg.Radio('Urban area','load',enable_events=True)
r3=sg.Radio('Rural area','load',enable_events=True)
r4=sg.Radio('Industrial area','load',enable_events=True)
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
          [sg.Submit('OK and return'),sg.Exit()]
          ]

# Create the window
window = sg.Window('Load Timeseries Generator', layout)
bids=['SE1','SE2','SE3','SE4']
seasons=['Winter','Autumn/Spring','Summer']
days=['Weekday','Weekend']

while True:
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
window.close()  