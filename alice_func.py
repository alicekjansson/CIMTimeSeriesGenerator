# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 10:02:31 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Medelårsförbrukning kWh
def forb():
    smahus=np.mean([6311,24166,20247,23456,23994,35254,18859,23927,30699,21951,22016,44637,21217])
    flerbostad=np.mean([187226,144237])
    industri=np.mean([102028,135285,169029,96287])
    medelforb=[smahus,flerbostad,industri]
    return medelforb

# Temperaturberoende
def tempberoende():
    smahus=np.mean([0.238,0.668,0.758,0.713,0.620,0.726,0.675,0.346,0.614,0.790,0.333,0.728,0.525])
    flerbostad=0.08*0.645 #Only 8% of apartment buildings heated with electricity
    industri=np.mean([0.532,0.563,0.240,0.578,0.576])
    medel=[smahus,flerbostad,industri]
    return medel

# Graddagar, SE1-SE4
def graddagar():
    se1=np.mean([5587,6693,5317,5324])
    se2=np.mean([4496,4748,4999,5082])
    se3=np.mean([3978,4094,3724,4451,4125,3307,3972,3910,3799,3777,3850,3646,3944,3527,3601,3896,3865])
    se4=np.mean([3325,3512,3265,3105,3653])
    graddag=[se1,se2,se3,se4]
    return graddag

# Import standard load curves
# För småhus är vanligaste uppvärmningssätt el, antingen direktverkande eller luftvärmepump. Även endast hushållsel tittas på (t.ex. fjärrvärme)
def load_df():
    df1=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_direktel.csv',delimiter=';')
    df1.index=df1['Hour']
    df1=df1.drop('Hour',axis=1)
    df1=df1[~df1.index.str.contains('std')].transpose() #Remove standard deviation data
    df2=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_hushallsel.csv',delimiter=';')
    df2.index=df2['Hour']
    df2=df2.drop('Hour',axis=1)
    df2=df2[~df2.index.str.contains('std')].transpose() #Remove standard deviation data
    df3=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_lagenhet.csv',delimiter=';')
    df3.index=df3['Hour']
    df3=df3.drop('Hour',axis=1)
    df3=df3[~df3.index.str.contains('std')].transpose() #Remove standard deviation data
    return [df1,df2,df3]

#Returns chosen load curve
def choose_curve(df,typ,elomr,arstid,dag):
    load_curve=df[typ].transpose()
    if dag == 0:
        load_curve = load_curve[load_curve.index.str.contains('Wday')]
    elif dag == 1:
        load_curve = load_curve[load_curve.index.str.contains('Wend')]
    if arstid == 0:
        load_curve = load_curve[load_curve.index.str.contains('Wint')]
    elif arstid == 1:
        load_curve = load_curve[load_curve.index.str.contains('Aut')]
    elif arstid == 2:
        load_curve = load_curve[load_curve.index.str.contains('Sum')]
    return load_curve.transpose()

#Return closest temperatures 
def choose_temp(load_curve,temp,arstid,elomr):
    load_temps=[float(el.split(':')[1]) for el in load_curve.columns]
    load_temps.sort()
    done=False
    for i,el in enumerate(load_temps):
        if temp<el:
            load_temps=[load_temps[i],load_temps[i-1]]
            done=True
            break
    if done == False:
        load_temps=load_temps[1:]
    load_temps=[load_temps,[i-1,i]]
    return load_temps