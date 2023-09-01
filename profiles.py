# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 16:07:07 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import numpy as np
from scipy.stats import norm
import warnings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
warnings.simplefilter(action='ignore', category=FutureWarning)


# Aggregate based on defined time = hour and cat = generation category
def aggregate_gen(df,time,cat,scale):
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
    return [el*scaling for el in year[cat]]


#Medelårsförbrukning kWh
def forb():
    smahus=np.mean([6311,24166,20247,23456,23994,35254,18859,23927,30699,21951,22016,44637,21217])
    flerbostad=np.mean([187226,144237])
    industri=np.mean([102028,135285,169029,96287])
    medelforb=[smahus,flerbostad,industri,smahus]
    return medelforb

# Temperaturberoende
def tempberoende():
    smahus=np.mean([0.668,0.758,0.713,0.620,0.726,0.675,0.346,0.614,0.790,0.333,0.728,0.525])
    flerbostad=0.08*0.645 #Only 8% of apartment buildings heated with electricity
    industri=0.578  #Minre industri med elvärme
    medel=[smahus,flerbostad,industri,0.238]
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
    df1=pd.read_csv(r'./Typkurvor/typkurvor_direktel.csv',delimiter=';')
    df1.index=df1['Hour']
    df1=df1.drop('Hour',axis=1)
    std1=df1[df1.index.str.contains('std')].transpose() #Save standard deviation data
    df1=df1[~df1.index.str.contains('std')].transpose() #Remove standard deviation data
    df2=pd.read_csv(r'./Typkurvor/typkurvor_hushallsel.csv',delimiter=';')
    df2.index=df2['Hour']
    df2=df2.drop('Hour',axis=1)
    std2=df2[df2.index.str.contains('std')].transpose() #Save standard deviation data
    df2=df2[~df2.index.str.contains('std')].transpose() #Remove standard deviation data
    df3=pd.read_csv(r'./Typkurvor/typkurvor_lagenhet.csv',delimiter=';')
    df3.index=df3['Hour']
    df3=df3.drop('Hour',axis=1)
    std3=df3[df3.index.str.contains('std')].transpose() #Save standard deviation data
    df3=df3[~df3.index.str.contains('std')].transpose() #Remove standard deviation data
    df4=pd.read_csv(r'./Typkurvor/typkurvor_industri.csv',delimiter=';')
    df4.index=df4['Hour']
    df4=df4.drop('Hour',axis=1).transpose()
    df4=df4*100
    return [df1,df3,df4,df2],[std1,std3,0,std2]

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
    return load_curve.transpose()/100
        

#Return closest temperatures 
def choose_temp(load_curve,temp,arstid,elomr):
    load_temps=[float(el.split(':')[1]) for el in load_curve.columns]
    load_temps.sort()
    maxi=len(load_temps)
    for i,el in enumerate(load_temps):
        if i==maxi-1:
            load_temps=load_temps[-2:]
            break
        if temp<el:
            if i==0:
                load_temps=[load_temps[0],load_temps[1]]
                break
            else:
                load_temps=[load_temps[i-1],load_temps[i]]
                break
    load_temps=[float(el) for el in load_temps]
    load_curve=load_curve.transpose()
    temp_curves=load_curve[load_curve.index.str.contains(str(load_temps[0])) | load_curve.index.str.contains(str(load_temps[1]))].transpose()
    return temp_curves, load_temps

#Transform load curve
def transform_load(load_curve,load_temps,Pav,temp,plot):
    P=pd.DataFrame(index=load_curve.index,columns=['P'])
    for i,row in load_curve.transpose().items():
        pnew=row.iloc[1]-((row.iloc[0]-row.iloc[1])/(load_temps[0]-load_temps[1])*(temp-load_temps[1]))
        P.loc[i,'P']=float(pnew)*Pav
    P2=P.copy()/Pav
    if plot ==True:
        fig,ax=plt.subplots(1,figsize=[8,4])
        load_curve.plot(ax=ax)
        P2.plot(ax=ax)
        ax.set_ylabel('Consumption [% of average load]')
        ax.set_title('Load curve')
        ax.set_xlabel('Hour')
        plt.xticks(rotation=45)
        plt.legend()
    return P

def generate_timeseries(typ,elomr,arstid,dag,plot):
    #Medelårsförbrukning kWh
    medelforb=forb()
    # Temperaturberoende
    psi=tempberoende()
    # Graddagar, SE1-SE4
    graddag=graddagar()
    # Calculate normalized annual energy and average load
    Ean=medelforb[typ]*(1+(psi[typ]*((graddag[elomr-1]/3978)-1)))
    Pav=Ean/8760
    # Import standard load curves
    # För småhus är vanligaste uppvärmningssätt el, antingen direktverkande eller luftvärmepump. Även endast hushållsel tittas på (t.ex. fjärrvärme)
    # df=load_df()
    df,std=load_df()
    #Define seasonal temperatures in se1-se4
    temperatur=pd.DataFrame(index=['Vinter','Höst/Vår','Sommar'],columns=['se1','se2','se3','se4'])
    temperatur['se1']=[-20,0,10]
    temperatur['se2']=[-20,0,15]
    temperatur['se3']=[-10,5,20]
    temperatur['se4']=[-5,10,20]
    # Select correct load curve and temperatures
    load_curve=choose_curve(df,typ,elomr,arstid,dag)
    temp=temperatur.iloc[arstid,elomr-1]
    load_curve,load_temps=choose_temp(load_curve,temp,arstid,elomr)
    #Transform load curve
    P=transform_load(load_curve,load_temps,Pav,temp,plot)
    return P


def aggregate_load(typ,elomr,arstid,dag,N):
    #Sammanlagringsfaktor
    S=[0.81,0.6,0.76,0.59]
    andel_elvarme=0.3       #Cirka 30% av småhus uppvärmda med elvärme enligt Energimyndighetens statistik 2021
    #Apartment or Industry
    if typ!=0:
        P=generate_timeseries(typ,elomr,arstid,dag,False)
        Ptot=P*S[typ]*N
    #Houses (both with and w/o electric heating)
    else:
        N_el=int(andel_elvarme*N)
        N_other=N-N_el
        P=generate_timeseries(3,elomr,arstid,dag,False)
        Ptot=P*S[3]*N_el
        P2=generate_timeseries(0,elomr,arstid,dag,False)
        Ptot2=P2*S[0]*N_other
        Ptot=Ptot+Ptot2         #Add load from both house types
    return Ptot


#Calculate number of dwellings based on share and scaling power level
def calculate_N(P_scale,share):
    P_scale=P_scale*1000    #From MW to kW
    mean=[]
    for typ in [0,1,2]:
        series=generate_timeseries(typ,4,0,0,False)
        mean.append(series.mean().iloc[0])
    #Solve equation system
    a = np.array([[mean[0], mean[1],mean[2]], [1-share[0], -share[0],-share[0]],[-share[1],1-share[1],-share[1]]])
    b = np.array([P_scale, 0,0])
    x = np.linalg.solve(a, b)
    x= [round(el) for el in x]
    return x
    
def fig_maker(curve,name):
    plt.clf()
    plt.close()
    plt.figure(figsize=(5,4))
    plt.plot(curve)    
    plt.xlabel('Power (MW)')
    plt.ylabel('Hour')  
    plt.title(name)
    plt.xticks(rotation=90)
    return plt.gcf() 

    
def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def delete_fig_agg(fig_agg):
    fig_agg.get_tk_widget().forget()
    plt.close('all')