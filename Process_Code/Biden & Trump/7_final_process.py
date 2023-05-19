#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 18:51:18 2023

@author: xintao
"""
import numpy as np
import pandas as pd
from datetime import datetime
import re
from dateutil.parser import parse

biden_basic_wod=pd.read_csv('../Data/Final_Data/Biden_basic_wod.csv',index_col=0)
trump_basic_wod=pd.read_csv('../Data/Final_Data/Trump_basic_wod.csv',index_col=0)
biden_basic_wod=biden_basic_wod.reset_index()
trump_basic_wod=trump_basic_wod.reset_index()
trump_basic_wod=trump_basic_wod.drop('index',axis=1)
biden_basic_wod=biden_basic_wod.drop('index',axis=1)

def make_final():
        cc=add_travel_info(trump_basic_wod)
        cc=add_countries_involved(cc)
        cc=add_accom(cc,'trump')
        cc=add_topics_orgs(cc)
        cc.to_csv('../Data/Final_Data/Trump_final.csv')
        cc=add_travel_info(biden_basic_wod)
        cc=add_countries_involved(cc)
        cc=add_accom(cc,'biden')
        cc=add_topics_orgs(cc)
        cc.to_csv('../Data/Final_Data/Biden_final.csv')
        return cc

def add_countries_involved(df):
    CON=['0']*len(df.index)
    for i,t in enumerate(df.Texts):
        countries=countries_in_it(t)
        count=''
        for c in countries:
            count=count+";;"+c
        CON[i]=count    
    df['Countries_inv']=CON
    return df
    
def add_travel_info(df):
    BD=[]
    ED=[]
    for i in range(len(df.index)):
        if df.Travel_kind[i]==0:
            BD.append(0)
            ED.append(0)      
        else:
            c=travel_dates(df.Dates[i],df.Texts[i])
            if c!=None:
                BD.append(c[0])
                ED.append(c[1])
            else:
                dates=datetime.strptime(df.Dates[i],"%d-%b-%y").date()
                BD.append(dates)
                ED.append(dates)
    df['Travel_Beg']=BD
    df['Travel_End']=ED
    return df

def add_accom(df,case):
    AC=[]
    AccWords=[' accompan',' join']
    for i in range(len(df.index)):
        tx=df.Texts[i]
        if any([s in tx for s in AccWords])==True: 
            kwp=[]
            for kw in AccWords:
                a=tx.find(kw)
                kwp.append(a)
            a=max(kwp)
            tx=tx[a:]
            lastname=find_lastname(tx,case)
            AC.append(lastname)
        else:
            AC.append(0)
    df['Accompanies']=AC  
    return df
              

""""""


def find_lastname(text, case):
    lowername_trump = ['Trump','Pence','Barsa', 'Bernicat', 'Biegun', 'Birx', 'Breier', 'Brownback', 'Brownfield', 'Bulatao', 'Chung',
                           'Cooper', 'Copper','Currie', 'Destro', 'Evanoff', 'Fannon', 'Foote', 'Ford', 'Friedt', 'Galt', 'Garber',
                           'Giuda', 'Goldstein', 'Green', 'Greenfield', 'Grunder', 'Guida', 'Hale', 'Haslach', 'Hook',
                           'Hushek', 'Jacobs', 'Jacobson', 'Kaidanow', 'Kozak', 'Krach', 'Lawler', 'Madison',
                           'Markgreen', 'McGuigan', 'Mcgurk','McGurk', 'Mitchell', 'Moley', 'Moore', 'Mull', 'Murphy', 'Nagy',
                           'Natali', 'Nauert', 'O’Connell', 'Palmieri', 'Phee', 'Poblete', 'Pompeo', 'Reeker', 'Risch',
                           'Royce', 'Russel', 'Sales', 'Schenker', 'Shannon', 'Singh', 'Stillwell', 'Stilwell', 'Sullivan', 'Taplin',
                           'Thompson', 'Thornton', 'Tillerson','TIllerson', 'Todd', 'Walsh', 'Wells', 'Wharton', 'Yamamoto', 'Yun']

    lowername_biden = ['Biden','Harris','Allen','Bernicat', 'Bitter', 'Blinken', 'Chung', 'Cormack', 'Donfried', 'Feltman', 'Fernandez', 'Godfrey',
                       'Hale', 'Hood', 'Jackson', 'Jenkins', 'Kang', 'Kerry', 'Kritenbrink', 'Leaf', 'Lempert', 'Lenderking',
                       'Lewis', 'Lu ', 'Lussenhop', 'Massinga', 'McKeon', 'Medina', 'Murray', 'Nichols', 'Noyes', 'Nuland','Patel',
                       'Peterson', 'Phee','Price', 'Power','Porter', 'Reeker', 'Robinson', 'Satterfield', 'Sherman', 'Sison', 'Smith',
                       'Steele', 'Stewart', 'Thompson', 'Toloui', 'Trudeau', 'Vallsnoyes', 'Walsh', 'Witkowsky', 'Yael',
                       'Zeya', 'Zuniga']
    if case=='trump':
        lowernames=lowername_trump
    if case=='biden':
        lowernames=lowername_biden
    lastname = []
    for name in lowernames:
            if name in str(text) or name.lower() in str(text):
                lastname = name
    if lastname==[]:
        lastname=0
    return lastname

def add_topics_orgs(df):
    R=len(df.index)
    T=[]
    O=[]
    P=[]
    for i in range(R):
        t1=str(df.Texts[i])
        texts=str(df.Texts[i])+str(df.content[i])
        T.append(topics_in_it(texts))
        O.append(orgs_inv(texts))
        if 'Trump' in texts or 'Biden' in t1:
            P.append(1)
        else:
            P.append(0)
    df['Topics']=T
    df['Orgs']=O
    df['Presidential']=P
    return df


                 
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
    
    
def travel_dates(dates,text):
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
         'Jan':1,
         'Feb':2,
         'Mar':3,
         'Jun':6,
         'Jul':7,
         'Aug':8,
         'Sept':9,
         'Oct':10,
         'Nov':11,
         'Dec':12,
         }
    if "travel to" not in text and 'travels to' not in text:
        if "on travel" not in text and 'accompanies' not in text and "to travel" not in text:
        #raise ValueError('No travel info in input!')
            mts
        else:
            tx=fix_dates(text)
            a1=tx.find('to travel')
            a2=tx.find('on travel')
            a=max(a1,a2)
            if a!=-1:
               a=a+10
            else:
               a=tx.find('accompanies')+12
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



def topics_in_it(text):
    # find topics in text
    topic=''
    strategic=['arms control','strategic','security','weapons','NATO','Defense']
    aid=['food','grain',' aid ','USAID','Red Cross', 'Humanitarian', 'Relief','U.S. Agency for International Development']
    tech=['technology',' 5g ',' ict ','artificial intelligence','biotech','bio-tech']
    health=['COVID','medical',' vaccine','hygiene','sanitation']  
    econ=['economic','trade','tariff','business','commerce','commercial','economy','investment']    
    nuke=['nuclear','proliferation']
    supply_chain=['supply chain','semi-conductor']
    climate=['climate','emission',' CO2 ','carbon']
    energy=['energy',' oil ', ' petro ', ' battery ']
    finance=['banking','finance','financial']

    if any([s.lower() in text.lower() for s in strategic])==True:
        topic=topic+';;StrategicSecurity'
    if any([s.lower() in text.lower() for s in aid])==True:
        topic=topic+';;Aid'
    if any([s.lower() in text.lower() for s in tech])==True:
        topic=topic+';;Tech'
    if any([s.lower() in text.lower() for s in health])==True:
        topic=topic+';;Health'
    if any([s.lower() in text.lower() for s in econ])==True:
        topic=topic+';;Econ'
    if any([s.lower() in text.lower() for s in nuke])==True:
        topic=topic+';;Nuke'
    if any([s.lower() in text.lower() for s in supply_chain])==True:
        topic=topic+';;Supply_chain'
    if any([s.lower() in text.lower() for s in climate])==True:
        topic=topic+';;Climate'
    if any([s.lower() in text.lower() for s in energy])==True:
        topic=topic+';;Energy'
    if any([s.lower() in text.lower() for s in finance])==True:
        topic=topic+';;Finance'
        
    return topic


  

def orgs_inv(text):
    ogs=''
    if 'NATO' in text:
        ogs=ogs+';;NATO'
    if ' USAID ' in text or 'U.S. Agency for International Development.' in text :
        ogs=ogs+';;USAID'  
    if ' WTO ' in text:
        ogs=ogs+';;WTO'
    if ' WHO ' in text:
        ogs=ogs+';;WHO'
    if ' UN ' in text or ' U.N. ' in text or ' United Nation'in text:
        ogs=ogs+';;UN;;'
    if 'ASEAN' in text:
        ogs=ogs+';;ASEAN' 
    if ' IMF' in text:
        ogs=ogs+';;IMF'
    if ' World Bank ' in text:
        ogs=ogs+';;World_Bank'
    if ' OPEC ' in text:
        ogs=ogs+';;OPEC'
    if ' IAEA ' in text:
        ogs=ogs+';;IAEA'  
    if 'G7' in text:
        ogs=ogs+';;G7'
    if 'G20 ' in text:
        ogs=ogs+';;G20'
    if ' UNICEF ' in text:
        ogs=ogs+';;UNICEF'
    if ' OECD ' in text:
        ogs=ogs+';;OECD'
    if ' COP' in text:
        ogs=ogs+';;COP'
    if ' Quad ' in text or ' QUAD' in text:
        ogs=ogs+';;Quad'
    if ' AUKUS ' in text or ' Aukus' in text:
        ogs=ogs+';;Aukus'   
    if " U.S. Embassy " in text:
        ogs=ogs+';;US Embassy'
    if " Pentagon " in text or ' Department of Defense' in text or ' DoD' in text:
        ogs=ogs+';;DOD(US)'   
    if " International Telecommunication Union " in text or ' ITU' in text:
        ogs=ogs+';;ITU'   
    if ' Red Cross' in text:
        ogs=ogs+';;Red Cross'
    if ' University' in text:
        ogs=ogs+';;University'  
    if ' African Union' in text:
        ogs=ogs+';;African Union'          
    if ' Mekong-U.S. Partnership' in text:
        ogs=ogs+';;Mekong-U.S. Partnership'   
    if ' C5+1' in text:
        ogs=ogs+';;C5+1'    
    if ' OSCE' in text:
        ogs=ogs+';;OSCE'                   
    if ' D-ISIS' in text:
        ogs=ogs+';;D-ISIS'      
    if ' Arctic Council' in text:
        ogs=ogs+';;Arctic Council'      
    if ' International Development Finance Corporation' in text or ' DoD' in text:
        ogs=ogs+';;IDFC'    
    if ' Technology Council' in text or ' DoD' in text:
        ogs=ogs+';;EU US Trade and Technology Council'   
        
    return ogs      


#def meettype
#def speechtype


    