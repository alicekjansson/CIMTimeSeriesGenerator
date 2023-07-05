# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 09:29:40 2023

@author: Alice
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Make choices

# 1. Småhus hushållsel
# 2. Småhus direktel
# 3. Lägenhet hushållsel
# 4. Lägenhet eluppvärmning

#Medelårsförbrukning kWh
def forb():
    smahus=np.mean([6311,24166,20247,23456,23994,35254,18859,23927,30699,21951,22016,44637,21217])
    flerbostad=np.mean([187226,144237])
    industri=np.mean([102028,135285,169029,96287])
    medelforb=[smahus,flerbostad,industri]
    return medelforb
medelforb=forb()

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

# Transform load curve

# Calculate new load curve