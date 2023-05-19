#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:05:26 2022

@author: xintao
"""

import numpy as np
import pandas as pd
from datetime import datetime
import re


def travel_destinations(text):
# Read info about travel destinations in text
    if "travel to" not in text and 'travels to' not in text:
        raise ValueError('No travel info in input!')
    else:
        tx=text
        a=tx.find('travel to')
        if a!=-1:
           a=a+10
        else:
           a=tx.find('travels to')+11
        b1=tx[a:].find(' from ')
        b2=tx[a:].find(' on ')
        b3=tx[a:].find('.')
        b4=tx[a:].find(' January')
        b5=tx[a:].find(' February') 
        b6=tx[a:].find(' March')
        b7=tx[a:].find(' April')
        b8=tx[a:].find(' May')
        b9=tx[a:].find(' June')
        b10=tx[a:].find(' July')
        b11=tx[a:].find(' August')  
        b12=tx[a:].find(' September')
        b13=tx[a:].find(' October')
        b14=tx[a:].find(' November')
        b15=tx[a:].find(' December')
        b16=tx[a:].find(' to ')
        if b1==-1:
            b1=1000
        if b2==-1:
            b2=1010
        if b3==-1:
            b3=1000
        if b4==-1:
            b4=1000
        if b5==-1:
            b5=1010
        if b6==-1:
            b6=1000
        if b7==-1:
            b7=1000
        if b8==-1:
            b8=1010
        if b9==-1:
            b9=1000
        if b10==-1:
            b10=1000
        if b11==-1:
            b11=1010
        if b12==-1:
            b12=1000
        if b13==-1:
            b13=1000
        if b14==-1:
            b14=1010
        if b15==-1:
            b15=1000
        if b16==-1:
            b16=1000
        b=min(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16)
        places=tx[a:a+b]
        return countries_in_it(places)

def fix_dates(text):
    # correct dates format and spelling in text
    month_list=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December', 'Oct']
    for mon in month_list:
        loc=text.find(mon)
        if loc!=-1:
            correct=text[loc-1:loc+len(mon)+1]
            if correct[-1]!=' ':
                # handles the case where space is missing
                text=text.replace(mon,mon+' ')
            if correct[0]!=' ':
                # handles the case where space is missing
                text=text.replace(mon,' '+mon)
    return text
        
            
def travel_dates(dates,text):
    # Read travel related dates in text
    dates=datetime.strptime(dates,"%d-%b-%y")
    mts={'January':1,
         'February':2,
         'March':3,
         'April':4,
         'May':5,
         'June':6,
         'July':7,
         'August':8,
         'September':9,
         'October':10,
         'November':11,
         'December':12,
         'Oct':11,
         }
    if "travel to" not in text and 'travels to' not in text:
        #raise ValueError('No travel info in input!')
        mts
    else:
        tx=fix_dates(text)
        a=tx.find('travel to')
        if a!=-1:
           a=a+10
        else:
           a=tx.find('travels to')+11
        tx=tx[a:]
        year_list=np.arange(1990,2030).astype(str)
        month_list=list(mts.keys())
        
        months=[]
        days=[]

        tx=tx.replace('–',' ')
        tx=tx.replace('-',' ')
        tx=tx.replace('—',' ')
        tx=tx.replace(',',' ')
        tx=tx.replace(';',' ')
        tx=tx.replace('.',' ')
        txl=tx.split(' ')
        for txi in txl:
            if txi.isdigit():
                if int(txi)<1000:
                    days.append(txi)
            if txi in  month_list:
                months.append(txi)
        monthdigit=[]  
        for mon in months:
            monthdigit.append(mts[mon])
            
        monthdigit=list(set(monthdigit))

        if len(monthdigit)==1 and len(days)==1:
            start_date=str(monthdigit[0])+'-'+days[0]
            end_date=str(monthdigit[0])+'-'+days[0]
            
        if len(monthdigit)==1 and len(days)==2:
            start_date=str(monthdigit[0])+'-'+days[0]
            end_date=str(monthdigit[0])+'-'+days[1]
            
        if len(monthdigit)==2 and len(days)==1:
                start_date=str(monthdigit[0])+'-'+days[0]
                end_date=str(monthdigit[1])+'-'+days[0]      
                
        if len(monthdigit)==2 and len(days)==2:
                start_date=str(monthdigit[0])+'-'+days[0]
                end_date=str(monthdigit[1])+'-'+days[1]
                
        if len(monthdigit)==1 and len(days)>2:
                start_date=str(monthdigit[0])+'-'+days[0]
                end_date=str(monthdigit[0])+'-'+days[-1]
        try: 
            start_date=start_date+'-'+str(dates.year)
            end_date=end_date+'-'+str(dates.year)
            start_date=datetime.strptime(start_date,"%m-%d-%Y").date()
            end_date=datetime.strptime(end_date,"%m-%d-%Y").date()
           
        except: 
           start_date=dates.date()
           end_date=dates.date()
        return start_date,end_date
                    

def countries_in_it(text):
    # find all countries in text
    country_lookup=pd.read_csv('../Data/Forms/country_lookup.csv',index_col=0)
    countries=[]
    for a in list(country_lookup.Names):
        if a in text:
            countries.append(a)
            
    for a in list(country_lookup.Full_Names):
        if a in text:
            c=country_lookup.Names[country_lookup.Full_Names==a]
            countries.append(list(c)[0])
            
    for a in list(country_lookup.Capital):
        if a in text:
            c=country_lookup.Names[country_lookup.Capital==a]
            countries.append(list(c)[0])
    for a in list(country_lookup.Adjs):
        if a in text:
            c=country_lookup.Names[country_lookup.Adjs==a]
            countries.append(list(c)[0])
    countries=list(set(countries))
    if len(countries)==0:
        return ['Domestic']
    else:
        return countries


      
def make_travel_places_rank_date():
    A=pd.read_csv('../Data/Mid_data/Trump/trump_3_line_processed.csv',index_col=0)
    Rank=pd.read_csv('../Data/Forms/ranks_trump.csv',index_col=1)
    places=[]
    start_dates=[]
    end_dates=[]
    types=[]
    Ranks=[]
    Topics=[]
    Meet_countries=[]
    for i,text in enumerate(A.Texts): 
        Topics.append(topics_in_it(text))
        Ranks.append(Rank.loc[A.Lastnames[i]].Rank)
        if "travel to" in text or 'travels to' in text:
            types.append('Travel')
            Meet_countries.append('')
        else:
            if 'attends meetings and briefings at the Department of State.' not in text and ('meet' in text.lower() or 'attend' in text.lower()):
                types.append('Meeting')
                countries_=countries_in_it(text)
                countries=''
                for country in countries_:
                    countries=countries+' ; '+country
                    
                Meet_countries.append(countries)
                
            else:
                types.append('TBD')
                Meet_countries.append('')
        try: 
            pl=travel_destinations(text)
            place=''
            for p in pl:
                place=place+' ; '+p
            places.append(place)
        
        except:places.append(' ')
        try: 
           start_date,end_date=travel_dates(A.Dates[i],text)
           start_dates.append(start_date)
           end_dates.append(end_date)
        except:
            start_dates.append('')
            end_dates.append('')
    A['Rank']=Ranks
    A['Type']=types
    A['Travel_Places']=places
    A['Travel_Start_Date']=start_dates
    A['Travel_End_Date']=end_dates
    A['Link_Content']=[' ']*len(A.Rank)
    A['Topics']=Topics
    A['Meet_countries']=Meet_countries
    A.to_csv('../Data/Mid_data/Trump/trump_4_test.csv') 
    
    A=pd.read_csv('../Data/Mid_data/Biden/biden_3_line_processed.csv',index_col=0)
    Rank=pd.read_csv('../Data/Forms/ranks_biden.csv',index_col=1)
    places=[]
    start_dates=[]
    end_dates=[]
    types=[]
    Ranks=[]
    Topics=[]
    Meet_countries=[]
    for i,text in enumerate(A.Texts):   
        Topics.append(topics_in_it(text))
        Ranks.append(Rank.loc[A.Lastnames[i]].Rank)
        if "travel to" in text or 'travels to' in text:
            types.append('Travel')
            Meet_countries.append('')
        else:
            if 'attends meetings and briefings at the Department of State.' not in text and ('meet' in text.lower() or 'attend' in text.lower()):
                types.append('Meeting')
                countries_=countries_in_it(text)
                countries=''
                for country in countries_:
                    countries=countries+' ; '+country
                    
                Meet_countries.append(countries)
            else:
                types.append('TBD')
                Meet_countries.append('')
        try:
            pl=travel_destinations(text)
            place=''
            for p in pl:
                place=place+' ; '+p
            places.append(place)
        
        except:places.append(' ')
        try: 
           start_date,end_date=travel_dates(A.Dates[i],text)
           start_dates.append(start_date)
           end_dates.append(end_date)
        except:
            start_dates.append('')
            end_dates.append('')
    A['Rank']=Ranks
    A['Type']=types
    A['Travel_Places']=places
    A['Travel_Start_Date']=start_dates
    A['Travel_End_Date']=end_dates
    A['Link_Content']=[' ']*len(A.Rank)
    A['Topics']=Topics
    A['Meet_countries']=Meet_countries
    A.to_csv('../Data/Mid_data/Biden/biden_4_test.csv')


def topics_in_it(text):
    # find topics in text
    topics=[]
    security=['arms control','strategic','security','weapons','NATO']
    sec_org=['NATO','AUKUS']
    food=['food','grain','rice']
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

make_travel_places_rank_date()