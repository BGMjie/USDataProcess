#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 23:56:45 2023

@author: xintao
"""
import numpy as np
import pandas as pd
from datetime import datetime
from difflib import SequenceMatcher
import jellyfish
from collections import Counter
import re

biden_basic_wod=pd.read_csv('../Data/Final_Data/Biden_basic_wod.csv',index_col=0)
trump_basic_wod=pd.read_csv('../Data/Final_Data/Trump_basic_wod.csv',index_col=0)

biden_basic_wod=biden_basic_wod.reset_index()
trump_basic_wod=trump_basic_wod.reset_index()
trump_basic_wod=trump_basic_wod.drop('index',axis=1)
biden_basic_wod=biden_basic_wod.drop('index',axis=1)


def fixtext(df,str1,str2):
    old_columns=list(df.columns)
    texts=list(df.Texts)
    df=df.drop('Texts',axis=1)
    for i,t in enumerate(texts):
        texts[i]=t.replace(str1,str2)
    df['Texts']=texts
    df=df.loc[:,old_columns]
    return df



def killline(df,num):
    df=df.drop(num)
    df=df.reset_index()
    df=df.drop('index',axis=1)
    return df



def similar(sentence1, sentence2):
    """
    Calculates the similarity between two sentences.
    """
    words1 = re.findall(r'\w+', sentence1.lower())
    words2 = re.findall(r'\w+', sentence2.lower())

    word_count1 = Counter(words1)
    word_count2 = Counter(words2)

    common_words = set(word_count1.keys()) & set(word_count2.keys())

    num_common_words = sum([word_count1[word] * word_count2[word] for word in common_words])

    denominator = (sum([word_count1[word]**2 for word in words1]) * sum([word_count2[word]**2 for word in words2]))**0.5

    if denominator == 0:
        return 0

    return num_common_words / denominator

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
    
def types(df):
    TVL=np.zeros(len(df.Texts))
    MET=np.zeros(len(df.Texts))
    TALK=np.zeros(len(df.Texts))
    travel=['travels','travel','travels to','travel to','tours ', 'tour ','visits ','visit','accompanies ','accompanied ','follows ','follow ', 'en route ']
    meet=['meets ','meet ','meeting ','attends ','attend ', ' met ','participates','participate', 'haslunch ', 'hosts ','host ','holds ','hold ','chairs ', 'dinner with', 'audience with ',' lunch with ',' leads ',' joins ',' join ',' lead ']
    talk=['a remark ','remarks ','speech ', 'talk ','addresses ', 'testifies ','speaks ', 'presents ', 'present ', 'testify ','briefs ','brief ','deliver ','delivers ']
    for i,text in enumerate(df.Texts):
        
        if any([s in text for s in travel])==True:
            TVL[i]=1
        if any([s.lower() in text.lower() for s in meet])==True:
            MET[i]=1
        if any([s.lower() in text.lower() for s in talk])==True:
            TALK[i]=1
    df['Travel_kind']=TVL
    df['Meet_kind']=MET
    df['Talk_kind']=TALK
    a=df.Travel_kind+df.Meet_kind+df.Talk_kind==0
    df['Other_kind']=a.astype(int)
    return df


def further_sim_check(df):
    sims=[]
    for i,t in enumerate(df.Texts):
        if i%20==0:
            print(i/len(df))
        maxj=min(len(df),i+40)
        for j,c in enumerate(df.Texts[i+1:maxj]):
            if similar(t,c)>0.91:
                sims.append([i,i+j+1])
    sims=sims
    bigsim=[]
    bigsimsum=[]
    for i,si in enumerate(sims):
        for j,sj in enumerate(sims):
            if i!=j and len(intersection(si,sj))>0:
                sb=list(set(list(si)+list(sj)))
                if sum(sb) not in bigsimsum:
                    bigsim.append(sb)
                    bigsimsum.append(sum(sb))
    addlist=list(np.arange(len(sims)))
    for i,sm in enumerate(sims):
        if sm[1] in np.array(bigsim).reshape(-1) or sm[0] in np.array(bigsim).reshape(-1):
            addlist.remove(i)
    sims=np.array(sims)
    sims=sims[addlist]
    oo=[]
    for s in sims:
        print(df.Texts[s])
        oo.append(list(s))
    sims=oo+list(bigsim)
    droplist=[]
    for s in sims:
        for k in s[1:]:
            droplist.append(k)
    df=df.drop(droplist)
    df=df.reset_index()
    df=df.drop('index',axis=1)
    return df
    

def find_duplicates_list(df):
   uniques=list(set(df.Texts))
   duplicates_t=[]
   duplicates_v=[]
   for u in uniques:
       l=sum(df.Texts==u)
       p=np.arange(len(df))[df.Texts==u]
       if l>1:
           duplicates_t.append(u)
           duplicates_v.append(p)
   duplicates=pd.DataFrame(duplicates_t,columns=['texts'])
   duplicates['positions']=duplicates_v
   return duplicates            

   
def reduce_by_text(df,texts):
    droplist=[]
    for i,t in enumerate(df.Texts):
        if texts in t:
            droplist.append(i)
    df=df.drop(droplist)
    df=df.reset_index()
    df=df.drop('index',axis=1)
    return df


def find_duplicates(df):
    duplicates=find_duplicates_list(df)
    droplist=[0]
    for dup in duplicates.positions:
        droplist=list(droplist)+list(dup[1:])
    droplist=droplist[1:]
    dup=np.zeros(len(df))
    dup[droplist]=1
    df['Duplicates']=dup
    return df
