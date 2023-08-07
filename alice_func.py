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
    df1=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_direktel.csv',delimiter=';')
    df1.index=df1['Hour']
    df1=df1.drop('Hour',axis=1)
    std1=df1[df1.index.str.contains('std')].transpose() #Save standard deviation data
    df1=df1[~df1.index.str.contains('std')].transpose() #Remove standard deviation data
    df2=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_hushallsel.csv',delimiter=';')
    df2.index=df2['Hour']
    df2=df2.drop('Hour',axis=1)
    std2=df2[df2.index.str.contains('std')].transpose() #Save standard deviation data
    df2=df2[~df2.index.str.contains('std')].transpose() #Remove standard deviation data
    df3=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_lagenhet.csv',delimiter=';')
    df3.index=df3['Hour']
    df3=df3.drop('Hour',axis=1)
    std3=df3[df3.index.str.contains('std')].transpose() #Save standard deviation data
    df3=df3[~df3.index.str.contains('std')].transpose() #Remove standard deviation data
    df4=pd.read_csv(r'C:/Users/Alice/OneDrive - Lund University/Dokument/GitHub/CIMProject/Typkurvor/typkurvor_industri.csv',delimiter=';')
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
    Ean=medelforb[typ]*(1+(psi[typ]*((graddag[elomr-1])/3978)-1))
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

def aggregate(typ,elomr,arstid,dag,N):
    #Sammanlagringsfaktor
    S=[0.81,0.6,0.76,0.59]
    andel_elvarme=0.3       #Cirka 30% av småhus uppvärmda med elvärme enligt Energimyndighetens statistik 2021
    Pall=pd.DataFrame()
    #Apartment or Industry
    if typ!=0:
        for i in range(N):
            P=generate_timeseries(typ,elomr,arstid,dag,False)
            Pall[i]=P
        Ptot=Pall.sum(axis=1)
        #If more than one object, add aggregation factor
        if N!=1:
            Ptot=Ptot*S[typ]
    #Houses (both with and w/o electric heating)
    else:
        N_el=int(andel_elvarme*N)
        N_other=N-N_el
        for i in range(N_el):
            P=generate_timeseries(3,elomr,arstid,dag,False)
            Pall[i]=P
        Ptot=Pall.sum(axis=1)
        #If more than one object, add aggregation factor
        if N!=1:
            Ptot=Ptot*S[3]
        Pall=pd.DataFrame()
        for i in range(N_other):
            P=generate_timeseries(0,elomr,arstid,dag,False)
            Pall[N_el+i]=P
        Ptot2=Pall.sum(axis=1)
        #If more than one object, add aggregation factor
        if N!=1:
            Ptot2=Ptot2*S[0]
        Ptot=Ptot+Ptot2         #Add load from both house types
    
    
    fig,ax=plt.subplots(1,figsize=[8,4])
    Ptot.plot(ax=ax)
    ax.set_xlabel('Hour')
    ax.set_ylabel('Total consumption (kW)')
    dwellings=['Småhus','Lägenhet','Industri']
    ax.set_title('Aggregated load')
    return Ptot