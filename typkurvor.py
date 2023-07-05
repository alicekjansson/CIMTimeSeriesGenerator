# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Make choices

# 0 Småhus
# 1 Lägenhet
# 2 Industri
typ=1

# Välj elområde
elomr=4

#Medelårsförbrukning kWh
def forb():
    smahus=np.mean([6311,24166,20247,23456,23994,35254,18859,23927,30699,21951,22016,44637,21217])
    flerbostad=np.mean([187226,144237])
    industri=np.mean([102028,135285,169029,96287])
    medelforb=[smahus,flerbostad,industri]
    return medelforb
medelforb=forb()

# Temperaturberoende
def tempberoende():
    smahus=np.mean([0.238,0.668,0.758,0.713,0.620,0.726,0.675,0.346,0.614,0.790,0.333,0.728,0.525])
    flerbostad=0.08*0.645 #Only 8% of apartment buildings heated with electricity
    industri=np.mean([0.532,0.563,0.240,0.578,0.576])
    medel=[smahus,flerbostad,industri]
    return medel
psi=tempberoende()

# Graddagar, SE1-SE4
def graddagar():
    se1=np.mean([5587,6693,5317,5324])
    se2=np.mean([4496,4748,4999,5082])
    se3=np.mean([3978,4094,3724,4451,4125,3307,3972,3910,3799,3777,3850,3646,3944,3527,3601,3896,3865])
    se4=np.mean([3325,3512,3265,3105,3653])
    graddag=[se1,se2,se3,se4]
    return graddag
graddag=graddagar()

# Calculate normalized annual energy and average load

Ean=medelforb[typ-1]/(1+psi[typ]*((graddag[elomr-1])/3978)-1)
Pav=Ean/8760

# Transform load curve

# Calculate new load curve