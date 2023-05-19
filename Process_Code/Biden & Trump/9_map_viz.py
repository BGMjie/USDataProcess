#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 22:26:42 2022

@author: xintao
"""
import numpy as np
import pandas as pd
from datetime import datetime
import re
import matplotlib.pyplot as plt
import geopandas as gpd

CP=pd.read_excel('Biden_Trump_Dip_Diff.xlsx',index_col=0)


world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

dif=[]
for name in world.name:
    try:dif.append(CP.loc[name].Rank_dif)
    except:dif.append(0)
world['rdif']=dif

dif=[]
for name in world.name:
    try:dif.append(CP.loc[name].Dif)
    except:dif.append(0)
world['dif']=dif

dif=[]
for name in world.name:
    try:dif.append(CP.loc[name].Biden)
    except:dif.append(0)
world['Biden']=dif

dif=[]
for name in world.name:
    try:dif.append(CP.loc[name].Trump)
    except:dif.append(0)
world['Trump']=dif

#world.plot(column='dif', cmap='RdBu')
world.plot(column='Trump')