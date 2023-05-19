#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 15:28:06 2022

@author: xintao
"""


import numpy as np
import pandas as pd
from datetime import datetime
import re


def topics_in_it(text):
    # find topics in text
    topics=[]
    security=['arms control','strategic','security','weapons','NATO']
    sec_org=['NATO','AUKUS']
    food=['food','grain']
    tech=['technology',' 5g ',' ict ','artificial intelligence']
    biotech=['COVID','medical',' vaccine','bio-tech','biotech','Hygiene','Sanitation']  
    econ=['economic','trade','tariff','business','commerce','economy','investment']   
    io=['International Development Finance Corporation',' World Bank ','health',' WTO ',' IMF ', ' ITU ','UNICEF','G7']   
    nuke=['nuclear','proliferation']
    supply_chain=['supply chain','semi-conductor']
    UN=[' UN ','U.N.','United Nation']
    ASEAN=['ASEAN ','IPEF ','CPTPP ','RECP ', 'Indo Pacific']
    climate=['climate','emission',' CO2 ','carbon']
    energy=['energy',' oil ', ' petro ', ' battery ']
    finance=['Banking','finance','financial']
    China=['chinese','china','taiwan','taiwanese','hong kong','tibet','xinjiang']
    
    if any([s.lower() in text.lower() for s in security])==True:
        topics.append('security')
    if any([s.lower() in text.lower() for s in food])==True:
        topics.append('food')
    if any([s.lower() in text.lower() for s in tech])==True:
        topics.append('tech')
    if any([s.lower() in text.lower() for s in biotech])==True:
        topics.append('bio-tech')
    if any([s.lower() in text.lower() for s in econ])==True:
        topics.append('econ')
    if any([s.lower() in text.lower() for s in io])==True:
        topics.append('international_organization')
    if any([s.lower() in text.lower() for s in nuke])==True:
        topics.append('nuke')
    if any([s.lower() in text.lower() for s in supply_chain])==True:
        topics.append('supply_chain')
    if any([s.lower() in text.lower() for s in climate])==True:
        topics.append('climate')
    if any([s.lower() in text.lower() for s in energy])==True:
        topics.append('climate')
    if any([s.lower() in text.lower() for s in finance])==True:
        topics.append('finance')
    if any([s.lower() in text.lower() for s in China])==True:
        topics.append('China')
    if any([s.lower() in text.lower() for s in sec_org])==True:
        topics.append('sec_org')
    if any([s.lower() in text.lower() for s in UN])==True:
        topics.append('UN')
    if any([s.lower() in text for s in ASEAN])==True:
        topics.append('ASEAN')
        
    topic=''
    for topic_ in topics:
        topic=topic+' ; '+topic_

    return topic


def add_topics():
    Biden=pd.read_csv('../Data/Mid_data/Biden/biden_5_with_link_content.csv',index_col=0)
    Trump=pd.read_csv('../Data/Mid_data/Trump/trump_5_with_link_content.csv',index_col=0)
    Biden=Biden.drop('Unnamed: 0',axis=1)
    Trump=Trump.drop('Unnamed: 0',axis=1)
    Topics=[]
    for i in Biden.index:
        Topics.append(topics_in_it(str(Biden.Texts[i])+' '+str(Biden.content[i])))
    Biden['Topics']=Topics
    Biden.to_csv('../Data/Mid_data/Biden/biden_6_final.csv')
   
    Topics=[]
    for i in Trump.index:
         Topics.append(topics_in_it(str(Trump.Texts[i])+' '+str(Trump.content[i])))   
    Trump['Topics']=Topics
    Trump.to_csv('../Data/Mid_data/Trump/trump_6_final.csv')
    
    
    
add_topics()