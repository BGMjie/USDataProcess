#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 12:28:18 2023

@author: xintao
"""
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
import os
import math
import spacy


'''@JIE 需要方程 1.5： 自动更新raw文件
        def update_raw(self): 
        update 'Raw_Data/'+self.president+'_output.txt', 'r', encoding='utf8'''   
'''@JIE 需要方程 3.12： 下载link列中的link并生成content列（content列名要小写哦）
        def update_linkcontent_col(self): '''
    
    
class Case:
    def __init__(self,president,save_mode=False,analysis_mode=True):
        
        '''
        解释：
        
        创造一个数据清理实例，用president选择清理方式，
        如果save_mode是True，会生成每一次操作的历史文件，建议只在调试时打开. 
        如果analysis_mode是True，可以使用高级分析方程（暂时还没写）
        最后一步 AUTO_COMPLETE是自动完成从Raw数据生成Final(Raw在Raw文件夹里，Final在Final文件夹里)
        Final文件的columns是大写的，和其它总统的Final一样
        其它中间步骤文件columns是小写的，为防止和Final窜文件（Precess文件夹里)
        使用起来先初始化 A=Case('Biden')
        之后用xxx功能直接用 A.xxx()就好
        
        方程功能如下
        --------------1.初步处理与储存工具---------------
        1.1 make_raw：创造原始Raw文件直接产生的DATE-TEXT表
        1.2 latest：返回最新文件的版本
        1.3 save：储存新版本到文件
        1.4 save_drop：储存最新一步中删掉的行到文件
        *** 1.5 自动更新raw文件（还没写）
        
        --------------2.文字行处理工具---------------
        
        2.1 remove_nan：删除空白行
        2.2 remove_by_texts：删除含有特定字符串的行
        2.3 remove_by_exact_texts：删除和特定字符串一样的行
        2.4 remove_ALL_CAPS：删除全部大写的行
        2.5 remove_orphan_links：删除多余的link行
        2.6 fix_orphan_links：删除多余的无主link行
        2.7 remove_links：将text列中link删除
        2.8 remove_duplicates：删除重复行
        2.9 fixtext：用str2替换行文本中的str1
        2.10 addtext：第n行文本后增加str1
        2.11 add_links：文本后增加原来应该有的link
        
        ---------------3.列生成工具---------------
        3.1 add_names_col：增加姓名列
        3.2 add_ranks_col：增加职级列
        3.3 add_titles_col：增加职称列
        3.4 add_counts：增加人数列
        3.5 add_travel_meet_kind：增加四个分类列
        3.6 add_countries_involved：增加相关国家列
        3.7 add_accom：增加陪同列
        3.8 add_topics_orgs：增加相关主题和组织列
        3.9 add_link_col：将行中link提取出来生成单列
        3.10 convertdate：将行中date改为datetime.date格式
        3.11 fixdate：用str2替换行日期列中的str1
        *** 3.12 下载link列中的link并生成content列 （还没写）
        
        -------------4.辅助工具---------------
        4.1 add_travel_info：找出旅行开始结束时间
        4.2 countries_in_it：返回文本中包含的国家
        4.3 find_lastname: 找到文本里的外交官
        4.4 find_lastname_lower：找到小写文本里的外交官
        4.5 find_lastnames：找到文本里的外交官
        4.6 topics_in_it：返回文本中包含的主题
        4.7 orgs_inv：返回文本中包含的组织
        4.8 travel_dates：识别文本中的旅行时间
        4.9 fix_dates：修好文本中的时间
        4.10 intersection：找到两个list的交集
        
        --------------5.最终生成工具---------------
        5.1 FINALIZE：把列名改好后存成final文
        5.2 AUTO_COMPLETE：自动完整清理，从Raw到Final
        
        
        --------------6.分析工具---------------
        6.1 when_who_where_what_travel 返回出访相关表格
        6.2 strangers 返回外交活动中非美人员
        6.3 when_who_where_what_meet 返回会面相关表格
        '''
        
        #president确定president
        presidents_list=['obama','trump','biden']
        president=president.lower()
        self.save_mode=save_mode
        if president not in  presidents_list:
            ValueError
            print('Error: Not a president name!')
        self.president=president
       #raw创造原始文件直接产生的DATE-TEXT表'''
        self.make_raw()
        #lasts临时储存上几次的表'''
        self.lasts=[] 
        self.maxi=self.latest()
        #制作国家-名称表
        self.country_lookup=pd.read_excel('Forms/country_lookup.xlsx',index_col=0)
        #制作外交官名-职位表
        self.titles=pd.read_excel('Forms/'+self.president+'_titles.xlsx',index_col=0)
        self.titles=dict(zip(self.titles.names,self.titles.title))
        #制作外交官名-职级表
        self.ranks=pd.read_excel('Forms/'+self.president+'_ranks.xlsx',index_col=0)
        self.ranks=dict(zip(self.ranks.Name,self.ranks.Rank))
        #current用来储存最新的结果
        try:self.current=pd.read_excel('Processed/'+self.president+'/'+self.president+'_'+str(self.latest())+'.xlsx',index_col=0)
        except:
            self.current=self.raw
            self.raw.to_excel('Processed/'+self.president+'/'+self.president+'_0.xlsx')
        name_trump = ['Barsa', 'Bernicat', 'Biegun', 'Birx', 'Breier', 'Brownback', 'Brownfield', 'Bulatao', 'Chung',
                               'Cooper', 'Copper','Currie', 'Destro', 'Evanoff', 'Fannon', 'Foote', 'Ford', 'Friedt', 'Galt', 'Garber',
                               'Giuda', 'Goldstein', 'Green', 'Greenfield', 'Grunder', 'Guida', 'Hale', 'Haslach', 'Hook',
                               'Hushek', 'Jacobs', 'Jacobson', 'Kaidanow', 'Kozak', 'Krach', 'Lawler', 'Madison',
                               'Markgreen', 'McGuigan', 'Mcgurk','McGurk', 'Mitchell', 'Moley', 'Moore', 'Mull', 'Murphy', 'Nagy',
                               'Natali', 'Nauert', 'O’Connell', 'Palmieri', 'Phee', 'Poblete', 'Pompeo', 'Reeker', 'Risch',
                               'Royce', 'Russel', 'Sales', 'Schenker', 'Shannon', 'Singh', 'Stillwell', 'Stilwell', 'Sullivan', 'Taplin',
                               'Thompson', 'Thornton', 'Tillerson','TIllerson', 'Todd', 'Walsh', 'Wells', 'Wharton', 'Yamamoto', 'Yun']
        name_biden = ['Allen','Bernicat', 'Bass ','Bitter', 'Blinken', 'Chung', 'Cormack', 'Chollet','Donfried', 'Feltman', 'Fernandez', 'Godfrey',
                           'Hale', 'Hood', 'Jackson', 'Jenkins', 'Kang', 'Kerry', 'Kritenbrink', 'Leaf', 'Lempert', 'Lenderking',
                           'Lewis', ' Lu ', 'Lussenhop', 'Massinga', 'McKeon', 'Medina', 'Murray', 'Nichols', 'Noyes', 'Nuland','Patel',
                           'Peterson', 'Phee','Price', 'Power','Porter', 'Reeker', 'Robinson', 'Satterfield', 'Sherman', 'Sison', 'Smith',
                           'Steele', 'Stewart', 'Stern','Thompson', 'Toloui', 'Trudeau', 'Vallsnoyes', 'Walsh', 'Witkowsky', 'Yael',
                           'Zeya', 'Zuniga','Pyatt']
        if president=='biden':
            self.names= name_biden
        if president=='trump':
            self.names= name_trump
        if analysis_mode==True:
           
            try:
                self.iDcN=pd.read_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_DATE_columns_Names_cell_Countries.xlsx',index_col=0)
                self.iDcC=pd.read_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_DATE_columns_Countries_cell_Names.xlsx',index_col=0)
                self.iCcN=pd.read_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Countries_columns_Names_cell_Days.xlsx',index_col=0)
            except:
                self.iDcN=None
                self.iDcC=None
   
    '''
    --------------1.初步处理与储存工具---------------
    1.1 make_raw：创造原始文件直接产生的DATE-TEXT表
    1.2 latest：返回最新文件的版本
    1.3 save：储存新版本到文件
    1.4 save_drop：储存最新一步中删掉的行到文件
    '''
    
    def make_raw(self):
        '''创造原始文件直接产生的DATE-TEXT表'''
        dates=[]
        lines=[]
        for line1 in open('Raw_Data/'+self.president+'_output.txt', 'r', encoding='utf8'):
            date = line1.split('\t')[0]
            str_all = line1.split('\t')[1]
            para = str_all.split(';;;;')
            for line in para:
                line = line.strip()
                dates.append(date)
                lines.append(line)
        self.raw=pd.DataFrame(dates,columns=['dates'])
        self.raw['text']=lines
        
    def latest(self):
        '''返回最新文件的版本'''
        try:
            files=os.listdir('Processed/'+self.president+'/')
            versions=[]
            try: files.remove('.DS_Store')
            except:files
            for file in files:
                if file[:1]!='~':
                    versions.append(int(file.split('_')[1].replace('.xlsx','')))
            maxi=max(versions)
        except:
            maxi=0
        return maxi
    
    def save(self):
        '''储存新文件的版本'''
        self.lasts.append(self.current)
        if len(self.lasts)>10:
            self.lasts=self.lasts[-9:]
        maxi=self.latest()
        self.current.to_excel('Processed/'+self.president+'/'+self.president+'_'+str(maxi+1)+'.xlsx')
        self.maxi=self.latest()
        
    def save_drop(self,dl):
           '''储存最新一步删掉的行'''
           dl.to_excel('Processed/Drop/'+self.president+'_'+str(self.maxi)+'_drop.xlsx')
        

    '''
    --------------2.文字行处理工具---------------
    
    2.1 remove_nan：删除空白行
    2.2 remove_by_texts：删除含有特定字符串的行
    2.3 remove_by_exact_texts：删除和特定字符串一样的行
    2.4 remove_ALL_CAPS：删除全部大写的行
    2.5 remove_orphan_links：删除多余的link行
    2.6 fix_orphan_links：删除多余的无主link行
    2.7 remove_links：将text列中link删除
    2.8 remove_duplicates：删除重复行
    2.9 fixtext：用str2替换行文本中的str1
    2.10 addtext：第n行文本后增加str1
    2.11 add_links：文本后增加原来应该有的link


    '''

    def remove_nan(self):
        '''删除空白行'''
        droplist=list(self.current.index[self.current.text.isna()])
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df
        if self.save_mode==True:
            self.save()
              
    def remove_by_texts(self,texts):
        '''删除含有特定字符串的行'''
        droplist=[]
        for i,t in enumerate(self.current.text):
            if texts in t:
                droplist.append(i)
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df
        if self.save_mode==True:
            self.save()
        
    def remove_by_exact_texts(self,texts):
        '''删除和特定字符串一样的行'''
        droplist=[]
        for i,t in enumerate(self.current.text):
            if texts == t:
                droplist.append(i)
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df
        if self.save_mode==True:
            self.save()
    
    def remove_ALL_CAPS(self):
        '''删除全部大写的行'''
        droplist=[]
        for i,t in enumerate(self.current.text):
            if t.isupper():
                droplist.append(i)
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df
        if self.save_mode==True:
            self.save()     

    def remove_orphan_links(self):
        '''删除多余的link行'''
        droplist=[]
        for i,t in enumerate(self.current.text):
            if t[:10]=='here<https' or t[:8]=='https://':
                if 'www.state.gov/' not in t:
                    droplist.append(i)
                    #print(i,t)
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df
        if self.save_mode==True:
            self.save()
    
    
    def fix_orphan_links(self):
        '''删除多余的无主link行'''
        droplist=[]
        for i,t in enumerate(self.current.text):
            if t[:10]=='here<https' or t[:8]=='https://':
                if 'www.state.gov/' in t:
                     r=0
                     for j,text in enumerate(self.current.text):
                         tt=t[t.find('.gov/')+5:t.find('/>')]
                         if tt in text and i!=j:
                             r=r+1
                     if r>0:
                         droplist.append(i)
        dl=self.current.loc[droplist]
        if self.save_mode==True:
            self.save_drop(dl)
        df=self.current.drop(droplist)
        df=df.reset_index()
        df=df.drop('index',axis=1)
        self.current=df        
        if self.save_mode==True:
            self.save()
                    
 
    def remove_links(self):
        '''将text列中link删除'''
        new_text=[]
        for i,t in enumerate(self.current.text):
            if '<' in t and '>' in t:
                s=[]
                e=[]
                links=[]
                for j,tt in enumerate(t):
                    if tt=='<':
                        s.append(j)
                    if tt=='>':
                        e.append(j)
                for k,ss in enumerate(s):
                    links.append(t[ss:e[int(k)]+1])
                for link in links:
                    t=t.replace(link,' ')
                new_text.append(t)           
            else:
                new_text.append(t)      
        old_columns=list(self.current.columns)
        df=self.current.drop('text',axis=1)
        df['text']=new_text
        df=df.loc[:,old_columns]
        self.current=df
        if self.save_mode==True:
            self.save()
           
    def remove_duplicates(self):
       '''删除重复行'''
       uniques=list(set(self.current.text))
       duplicates_t=[]
       duplicates_v=[]
       for u in uniques:
           l=sum(self.current.text==u)
           p=np.arange(len(self.current.text))[self.current.text==u]
           if l>1:
               duplicates_t.append(u)
               duplicates_v.append(p)
       duplicates=pd.DataFrame(duplicates_t,columns=['texts'])
       duplicates['positions']=duplicates_v
       droplist=[]
       for pos in duplicates.positions:
           droplist= droplist+list(pos[:-1])
       dl=self.current.loc[droplist]
       if self.save_mode==True:
            self.save_drop(dl)
       df=self.current.drop(droplist)
       df=df.reset_index()
       df=df.drop('index',axis=1)
       self.current=df        
       if self.save_mode==True:
            self.save()

            
    def fixtext(self,str1,str2):
        '''用str2替换行文本中的str1'''
        old_columns=list(self.current.columns)
        texts=list(self.current.text)
        df=self.current.drop('text',axis=1)
        for i,t in enumerate(texts):
            texts[i]=t.replace(str1,str2)
        df['text']=texts
        df=df.loc[:,old_columns]
        self.current=df
        if self.save_mode==True:
            self.save()
        
    def addtext(self,ind,str1):
        '''第n行文本后增加str1'''
        old_columns=list(self.current.columns)
        texts=list(self.current.text)
        df=self.current.drop('text',axis=1)
        texts[ind]=texts[ind]+str1
        df['text']=texts
        df=df.loc[:,old_columns]
        self.current=df
        if self.save_mode==True:
            self.save()
            
    def add_links(self):
        '''文本后增加原来应该有的link'''
        for i,t in enumerate(self.current.text):
            if t[:10]=='here<https' or t[:8]=='https://':
                if 'www.state.gov/' in t:
                    scores=np.zeros(20)
                    namematches=np.zeros(20)
                    matchlines=self.current.text[max(0,i-10):min(i+10,len(self.current.text))]
                    t_name=self.find_lastname(t)
                    tt=t[t.find('.gov/')+5:t.find('/>')].split('-')
                    try: tt.remove('secretary')
                    except:tt
                    try: tt.remove('under')
                    except:tt
                    try: tt.remove('deputy')
                    except:tt
                    try: tt.remove('assistant')
                    except:tt
                    try: tt.remove('to')
                    except:tt       
                    try: tt.remove('travel')
                    except:tt    
                    for k,line in enumerate(matchlines):
                        scores[k]=len(self.intersection(list(set(line.lower().split(' '))),tt))/len(tt)
                        name=self.find_lastname(line)
                        if t_name == name:
                            namematches[k]=1
                    maxi=np.argmax(scores)
                    maxx=np.max(scores)
                    big=self.current.text[max(0,i-10)+maxi]
                    if maxx>0.3 and namematches[maxi]==1 and t not in big:
                        #print(max(0,i-10)+maxi)
                        text=' '+t
                        self.addtext(max(0,i-10)+maxi,text)
 

    
            
    '''
    ---------------3.列生成工具---------------
    3.1 add_names_col：增加姓名列
    3.2 add_ranks_col：增加职级列
    3.3 add_titles_col：增加职称列
    3.4 add_counts：增加人数列
    3.5 add_travel_meet_kind：增加四个分类列
    3.6 add_countries_involved：增加相关国家列
    3.7 add_accom：增加陪同列
    3.8 add_topics_orgs：增加相关主题和组织列
    3.9 add_link_col：将行中link提取出来生成单列
    3.10 convertdate：将行中date改为datetime.date格式
    3.11 fixdate：用str2替换行日期列中的str1
    '''
             
        
    def add_names_col(self):
        '''增加姓名列'''
        lnames=[]
        for i,t in enumerate(self.current.text):
            name=self.find_lastname(t)
            name1=self.find_lastname_lower(self.current.links[i])
            if name!=[]:
                if name1==[]:
                    name=[name]
                else:
                    name=[name,name1]
            else:
                if name1!=[]:
                    name=[name1]
            name=list(set(name))
            if len(name)>1:
                names=self.find_lastnames(t[:int(len(t)/2.2)])
                name=names[0]
            if type(name)==list:
                if len(name)>0:
                    lnames.append(name[0])
                else:
                    lnames.append('Blinken')
            else:
                    lnames.append(name)
        old_columns=list(self.current.columns)
        self.current['lastnames']=lnames
        old_columns=list(old_columns[:1]+['lastnames']+old_columns[1:])
        self.current=self.current[old_columns]
        if self.save_mode==True:
            self.save()

        
    def add_ranks_col(self):   
       '''增加职级列'''
       ranks=[]
       for i,name in enumerate(self.current.lastnames):
           ranks.append(self.ranks[name])

       old_columns=list(self.current.columns)
       self.current['ranks']=ranks
       old_columns=list(old_columns[:3]+['ranks']+old_columns[3:])
       self.current=self.current[old_columns]
       if self.save_mode==True:
            self.save()
    
    def add_titles_col(self):   
       '''增加职称列'''
       titles=[]
       for i,name in enumerate(self.current.lastnames):
           titles.append(self.titles[name])

       old_columns=list(self.current.columns)
       self.current['titles']=titles
       old_columns=list(old_columns[:2]+['titles']+old_columns[2:])
       self.current=self.current[old_columns]
       if self.save_mode==True:
            self.save()
    
    def add_counts(self):   
       '''增加人数列'''
       counts=[]
       for i,text in enumerate(self.current.text):
           names=self.find_lastnames(text)
           counts.append(len(names))
       self.current['counts']=counts
       if self.save_mode==True:
            self.save()

    def add_travel_meet_kind(self):    
       '''增加分类列'''
       TVL=np.zeros(len(self.current.text))
       MET=np.zeros(len(self.current.text))
       TALK=np.zeros(len(self.current.text))
       travel=['travels','travel','travels to','travel to','tours ', 'tour ','visits ','visit','accompanies ','accompanied ','follows ','follow ', 'en route ']
       meet=['meets ','meet ','meetswith','lunch with','receives',' sign ',' photo with ','meeting ','attends ','attend ', ' met ','participates','participate', 'haslunch ', 'hosts ','host ','co-host','holds ','hold ','chairs ', 'dinner with', 'audience with ',' lunch with ',' leads ',' joins ',' join ',' lead ']
       talk=['a remark ','remarks ','speech ', 'talk ','provides an update ','moderates','addresses ', 'testifies ','speaks ', 'presents ', 'present ', 'testify ','briefs ','brief ','deliver ','delivers ']
       for i,text in enumerate(self.current.text):
           if any([s in text for s in travel])==True:
                TVL[i]=1
           if any([s.lower() in text.lower() for s in meet])==True:
                MET[i]=1
           if any([s.lower() in text.lower() for s in talk])==True:
                TALK[i]=1
       self.current['travel_kind']=TVL
       self.current['meet_kind']=MET
       self.current['talk_kind']=TALK
       a=self.current.travel_kind+self.current.meet_kind+self.current.talk_kind==0
       self.current['other_kind']=a.astype(int)
       if self.save_mode==True:
            self.save()
            
    def add_countries_involved(self):
        '''增加相关国家列'''
        CON=['0']*len(self.current.index)
        for i,t in enumerate(self.current.text):
            countries=self.countries_in_it(t)
            count=''
            for c in countries:
                count=count+";;"+c
            CON[i]=count    
        self.current['countries_inv']=CON
        if self.save_mode==True:
            self.save()

            
    def add_accom(self):
        '''增加陪同列'''
        ACC=[]
        for i,t in enumerate(self.current.text):
            dp=[]
            dp=dp+self.find_lastnames(t)
            if 'Trump' in t:
                dp.append('Trump')
            if 'Biden' in t:
                dp.append('Biden')
            try: dp.remove(self.current.lastnames[i])
            except:
                dp
            if len(dp)==0:
                ACC.append('')
            else:
                c=';;'
                for d in dp:
                    c=c+d+';;'
                ACC.append(c)

        self.current['accompanies']=ACC
        if self.save_mode==True:
            self.save()

    def add_topics_orgs(self):
        '''增加相关主题和组织列'''
        R=len(self.current.index)
        T=[]
        O=[]
        P=[]
        for i in range(R):
            t1=str(self.current.text[i])
            texts=str(self.current.text[i])#+str(df.content[i])
            T.append(self.topics_in_it(texts))
            O.append(self.orgs_inv(texts))
            if 'Trump' in texts or 'Biden' in t1:
                P.append(1)
            else:
                P.append(0)
        self.current['topics']=T
        self.current['orgs']=O
        self.current['presidential']=P
        if self.save_mode==True:
            self.save()



    def add_link_col(self):
        '''将行中link提取出来单列行'''
        link_col=[]
        for i,t in enumerate(self.current.text):
            if '<' in t and '>' and 'www.state.gov'in t:
                s=[]
                e=[]
                links=[]
                for j,tt in enumerate(t):
                    if tt=='<':
                        s.append(j)
                    if tt=='>':
                        e.append(j)
                for k,ss in enumerate(s):
                    links.append(t[ss:e[int(k)]+1])
                link=links[-1]
                link_col.append(link)
            else:
                link_col.append('')
        self.current['links']=link_col
        if self.save_mode==True:
            self.save()

    def convertdate(self):
        '''将dates转成datetime,date'''
        old_columns=list(self.current.columns)
        dates=list(self.current.dates)
        dates_new=[]
        df=self.current.drop('dates',axis=1)
        for i,t in enumerate(dates):
            dates_new.append(datetime.strptime(t,"%B %d, %Y").date())
        df['dates']=dates_new
        df=df.loc[:,old_columns]
        self.current=df
        if self.save_mode==True:
            self.save()

    def fixdate(self,str1,str2):
        '''用str2替换行日期中的str1'''
        old_columns=list(self.current.columns)
        dates=list(self.current.dates)
        df=self.current.drop('dates',axis=1)
        for i,t in enumerate(dates):
            dates[i]=t.replace(str1,str2)
        df['dates']=dates
        df=df.loc[:,old_columns]
        self.current=df
        if self.save_mode==True:
            self.save()
            
    
        
        
    '''
    -------------4.辅助工具---------------
    4.1 add_travel_info：找出旅行开始结束时间
    4.2 countries_in_it：返回文本中包含的国家
    4.3 find_lastname: 找到文本里的外交官
    4.4 find_lastname_lower：找到小写文本里的外交官
    4.5 find_lastnames：找到文本里的外交官
    4.6 topics_in_it：返回文本中包含的主题
    4.7 orgs_inv：返回文本中包含的组织
    4.8 travel_dates：识别文本中的旅行时间
    4.9 fix_dates：修好文本中的时间
    4.10 intersection：找到两个list的交集
    
    '''
        
    def add_travel_info(self):
        '''找出旅行开始结束时间'''
        BD=[]
        ED=[]
        for i in range(len(self.current.index)):
            if self.current.travel_kind[i]==0:
                BD.append(0)
                ED.append(0)      
            else:
                c=self.travel_dates(self.current.dates[i],self.current.text[i])
                if c!=None:
                    BD.append(c[0])
                    ED.append(c[1])
                else:
                    try:
                        dates=self.current.dates[i].date()
                    except:
                        dates=self.current.dates[i]
                    BD.append(dates)
                    ED.append(dates)
        self.current['travel_beg']=BD
        self.current['travel_end']=ED
        if self.save_mode==True:
            self.save()
            
    def countries_in_it(self,text):
        '''返回文本中包含的国家'''
        # find all countries in text
        
        countries=[]
        for a in list(self.country_lookup.Names):
            if a in text:
                countries.append(a)            
        for a in list(self.country_lookup.Full_Names):
            if a in text:
                c=self.country_lookup.Names[self.country_lookup.Full_Names==a]
                countries.append(list(c)[0])
                
        for a in list(self.country_lookup.Capital):
            if a in text:
                c=self.country_lookup.Names[self.country_lookup.Capital==a]
                countries.append(list(c)[0])
        for a in list(self.country_lookup.Adjs):
            if a in text:
                c=self.country_lookup.Names[self.country_lookup.Adjs==a]
                countries.append(list(c)[0])
        countries=list(set(countries))
        if len(countries)==0:
            return ['Domestic']
        else:
            return countries
    
        

    def find_lastname(self,text):
        '''找到文本里的外交官'''
        # returns the last names included in str, [] means the str has no relevant name in it.
        lastname = []
        for name in self.names:
            if name in str(text):
                lastname = name.strip()
        # 处理各种同名的问题       
        if lastname=='Trudeau' and 'Blinken' in text:
            lastname='Blinken'
        if lastname=='Trudeau' and 'Sherman' in text:
            lastname='Sherman'
        if lastname=='Fernandez' and 'Blinken' in text and 'Argent' in text:
            lastname= 'Blinken'
        if lastname=='Sherman' and 'Donfried' in text and 'Mercedes' in text:
            lastname= 'Donfried'
        if lastname=='Stewart' and 'Donfried' in text and 'Cyprus' in text:
            lastname= 'Donfried'
        if lastname=='Stern' and 'Donfried' in text and 'Maram' in text:
            lastname= 'Donfried'
        if lastname=='Chung' and 'Blinken' in text and 'Korea' in text:
            lastname= 'Blinken'
        if lastname=='Power' and 'Bernicat' in text and 'Powering' in text:
            lastname= 'Bernicat'
        if lastname=='Kang' and 'Blinken' in text and 'Kangerlussuaq' in text:
            lastname= 'Blinken'
        return lastname

    def find_lastname_lower(self,text):
        '''找到文本里的外交官小写'''
        # returns the last names included in str, [] means the str has no relevant name in it.
        lastname = []
        for name in self.names:
            if name.lower() in str(text):
                lastname = name.strip()
        return lastname


    def find_lastnames(self,text):
        '''找到文本里的所有外交官'''
        # returns the last names included in str, [] means the str has no relevant name in it.
        lastnames = []
        for name in self.names:
            if name in str(text):
                # 处理各种同名的问题     
                lastnames.append(name.strip())
                if name =='Trudeau' and "Canad" in text:
                   #print('Canadian Exception')         
                   lastnames.remove('Trudeau')
                if name =='Fernandez' and "Argent" in text:
                   #print('Argentina Exception')
                   lastnames.remove('Fernandez')
                if name =='Sherman' and 'Mercedes' in text:
                   #print('Benz Exception')        
                   lastnames.remove('Sherman')
                if name =='Stewart' and 'Cyprus' in text:
                   #print('Cyprus Exception')
                   lastnames.remove('Stewart')
                if name=='Stern' and 'Maram' in text:
                   #print('Maram Exception')  
                   lastnames.remove('Stern')
                if name=='Chung' and 'Korea' in text:
                   #print('Korea Exception')
                   lastnames.remove('Chung')
                if name=='Power' and 'Powering' in text:
                   #print('Power Exception')
                   lastnames.remove('Power')
                if name=='Kang' and 'Kangerlussuaq' in text:
                   #print('Kangerlussuaq Exception')
                   lastnames.remove('Kang')

                        
        return lastnames
    
    def topics_in_it(self,text):
        '''返回文本中包含的主题'''
        # find topics in text
        topic=''
        strategic=['arms control','strategic','security','weapons','NATO','Defense']
        aid=['food','grain',' aid ','USAID','Red Cross', 'Humanitarian', 'Relief','U.S. Agency for International Development']
        tech=['technology',' 5g ',' ict ',' Cyber','digital','semiconductor','CHIPS','artificial intelligence','biotech','bio-tech']
        health=['COVID','medical',' vaccine','hygiene','sanitation']  
        econ=['economic','trade','tariff','business','commerce','commercial','economy','investment']    
        nuke=['nuclear','proliferation','Nuclear','NPT review','Atomic']
        supply_chain=['supply chain','semi-conductor']
        climate=['climate','emission',' CO2 ','carbon']
        energy=['energy',' oil ', ' petro ', ' battery ']
        finance=['banking','finance','financial']
        atlantic=['Transatlantic','transatlantic','atlantic',' Atlantic']
        LGBT=['LGBT']
        female=['Women', 'Girl', 'female','woman']
        Chinese_areas=['tibet','taiwan','uyghur','hong kong','china sea']
        
    
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
        if any([s.lower() in text.lower() for s in atlantic])==True:
            topic=topic+';;Atlantic'
        if any([s.lower() in text.lower() for s in LGBT])==True:
            topic=topic+';;LGBT'  
        if any([s.lower() in text.lower() for s in female])==True:
            topic=topic+';;Female'  
        if any([s.lower() in text.lower() for s in Chinese_areas])==True:
            topic=topic+';;Chinese_areas'  
        return topic

  
    def orgs_inv(self,text):
        '''返回文本中包含的组织'''
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
        if ' OECD ' in text or 'Organization for Security and Co-operation in Europe' in text:
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
        if "International Telecommunication Union" in text or ' ITU' in text:
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
        if '  EU ' in text or ' European Union ' in text or ' European Commission ' in text or ' European Parliament ' in text:
            ogs=ogs+';;EU'  
        if ' MCC ' in text or 'Millennium Challenge Corporation' in text:
            ogs=ogs+';;MCC'   
        if 'Pacific Island' in text:
            ogs=ogs+';;Pacific Islands'         
        if ' WHO ' in text or 'World Health Organization' in text:
            ogs=ogs+';;WHO'  
        if ' Executive Council on Diplomacy ' in text:
            ogs=ogs+';;Executive Council on Diplomacy'  
        if ' Gulf Cooperation Council ' in text or 'GCC' in text:
            ogs=ogs+';;Gulf Cooperation Council' 
        if ' Alliance for Development in Democracy' in text:
            ogs=ogs+';;Alliance for Development in Democracy'             
        if ' European Investment Bank' in text:
            ogs=ogs+';;European Investment Bank'            
        if 'U.S. Trade and Development Agency' in text  or 'USTDA' in text:
            ogs=ogs+';;USTDA'   
        if 'Indo-Pacific Economic Framework' in text  or 'IPEF' in text:
            ogs=ogs+';;IPEF'      

            
            
            
            
        return ogs  
    
    def travel_dates(self,dates,text):
       '''识别文本中的旅行时间'''
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
               tx=self.fix_dates(text)
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
           tx=self.fix_dates(text)
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
              start_date=dates
              end_date=dates

      
           return start_date,end_date


    def fix_dates(self,text):
        '''修好文本中的时间'''
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

    def intersection(self,lst1, lst2):
        '''找到两个list的交集'''
        lst3 = [value for value in lst1 if value in lst2]
        return lst3
      


    '''
    --------------5.最终生成工具---------------
    5.1 FINALIZE：把列名改好后存成final文件，Final文件的columns是大写的，和其它总统的Final一样
    5.2 AUTO_COMPLETE：自动完整清理，从Raw到Final
    
    '''
  
    
    def FINALIZE(self):
        '''把列名改好后存成final文件'''
        fromc=['dates', 'lastnames', 'titles', 'ranks', 'text', 'content','links', 'counts',
               'travel_kind', 'meet_kind', 'talk_kind', 'other_kind', 'travel_beg',
               'travel_end', 'countries_inv', 'accompanies', 'topics', 'orgs',
               'presidential']
        toc=['Dates', 'Lastnames', 'Title', 'Rank', 'Texts', 'content', 'Links',
               'Counts', 'Travel_kind', 'Meet_kind', 'Talk_kind', 'Other_kind',
               'Travel_Beg', 'Travel_End', 'Countries_inv', 'Accompanies', 'Topics',
               'Orgs', 'Presidential']
        fromto=dict(zip(fromc,toc))
        new_col=[]
        for a in list(self.current.columns):
            new_col.append(fromto[a])
            
        final=self.current.copy()
        final.columns=new_col
        final.to_excel('Final/'+self.president+'/'+self.president.capitalize()+'_final.xlsx')
        
    def AUTO_COMPLETE(self):
        '''自动完整清理'''
        self.current=self.raw
        self.remove_nan()
        self.remove_ALL_CAPS()
        print('Nan and CAPs removed')
        self.remove_by_texts('***')
        self.remove_by_texts('No Department Press Briefing.')
        self.remove_by_texts('No Department press briefing.')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and www.YouTube.com/statedept<http://www.YouTube.com/statedept>.')
        self.remove_by_texts('attends meetings and briefings at the Department of State.')
        self.remove_by_texts('rd Street Entrance Lobby.')
        self.remove_by_texts('Department Press Briefing.')
        self.remove_by_texts('Department Press Briefing')
        self.remove_by_texts('www.state.gov<https://www.state.gov/> and www.youtube.com/statedept<https://www.youtube.com/statedept>')
        self.remove_by_texts('whas no public appointments')
        self.remove_by_texts('has no public appointments')
        self.remove_by_texts('will be livestreamed on')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and www.youtube.com/statedept<http://www.youtube.com/statedept>.')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and www.youtube.com/statedept<http://www.youtube.com/statedept>')
        self.remove_by_texts('Department Briefing.')
        self.remove_by_texts('Thank you for visitingstate.gov.')
        self.remove_by_texts('www.state.gov<http://www.state.gov/> andwww.YouTube.com/statedept<http://www.YouTube.com/statedept/>.')
        self.remove_by_texts('www.state.gov<https://www.state.gov/> and www.youtube.com/statedept.<https://www.youtube.com/statedept>')
        self.remove_by_texts('www.state.gov<http://www.state.gov>andwww.YouTube.com/StateDept<http://www.YouTube.com/StateDept/>.')
        self.remove_by_texts('attends meetings and briefings, at the Department of State.')
        self.remove_by_texts('www.state.gov<https://www.state.gov/>.')
        self.remove_by_texts('Preset time for video cameras is at')
        self.remove_by_texts('www.state.gov<http://www.state.gov/> and www.youtube.com/statedept<http://www.youtube.com/statedept>.')
        self.remove_by_texts('www.state.gov<http://www.state.gov/>andwww.youtube.com/statedept<https://gcc02.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.youtube.com%2Fstatedept&data=05%7C01%7CWoolfolkAM2%40state.gov%7C460bac93a67d47c2438d08db03d030fb%7C66cf50745afe48d1a691a12b2121f44b%7C0%7C0%7C638107964924158550%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=D4S0nVrT7Wp28GoLevND%2FL%2BunBFaNlnF4KG0U5fKoL4%3D&reserved=0>.')
        self.remove_by_texts('www.state.gov<http://www.state.gov>andwww.youtube.com/statedept<https://gcc02.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.youtube.com%2Fstatedept&data=05%7C01%7CSaylesAG%40state.gov%7C57f2ce5f24c14e72d11d08dab15baac3%7C66cf50745afe48d1a691a12b2121f44b%7C0%7C0%7C638017304503281944%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=Q3WkHrBOEKseVDm2FhYpwhJrVpVPn3oUtLP15MwmUTs%3D&reserved=0>.')
        self.remove_by_texts('www.state.gov<http://www.state.gov/> andwww.youtube.com/statedept<')
        self.remove_by_texts('The Department is closed')
        self.remove_by_texts('Press Briefing with')
        self.remove_by_texts('a press availability')
        self.remove_by_texts('will be live-streamed on')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and www.youtube.com/statedept<')
        self.remove_by_texts('attends meetings and briefings, from the Department of State.')
        self.remove_by_texts('www.state.gov<http://www.state.gov>.')
        self.remove_by_texts('will be live streamed on')
        self.remove_by_texts('press briefing')
        self.remove_by_texts('Preset time and final access')
        self.remove_by_texts('www.state.gov<https://mcas-proxywe')
        self.remove_by_texts('www.state.gov<http://www.state.gov>andwww.YouTube.com/statedept<https://www.youtube.com/statedept>')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and https://media.un.org/en/webtv<https://media.un.org/en/webtv>.')
        self.remove_by_texts('Cross International Date Line')
        self.remove_by_texts('camera spray will be')
        self.remove_by_texts('www.state.gov<http://www.state.gov> and https://www.youtube.com/user/statevideo<https://www.youtube.com/user/statevideo>')
        self.remove_by_texts('www.state.gov<https://www.state.gov/> and www.YouTube.com/statedept<https://www.youtube.com/statedept>.')
        self.remove_by_texts('streamed on')
        self.remove_by_texts('www.state.gov<http://www.state.gov/>.')
        self.remove_by_texts('attends meeting and briefings.')
        self.remove_by_texts('attends meeting and briefings')
        self.remove_by_texts('attends meetings and briefings')
        self.remove_by_texts('https://www.youtube.com/user/statevideo<https://www.youtube.com/user/statevideo>.')
        self.remove_by_texts('UN Web TV<http://webtv.un.org/>.')
        self.remove_by_texts('https://arctic-council.org/en/resources/reykjavik/<https://arctic-council.org/en/resources/reykjavik/>.')
        self.remove_by_texts('U.S. Department of State – YouTube<https://www.youtube.com/user/statevideo>.')
        self.remove_by_texts('here<http://www.orfonline.org/Raisina-dialogue/>')
        self.remove_by_texts('no Department briefing')
        self.remove_by_texts('Preset time')
        self.remove_by_texts('www.state.gov<http://www.state.gov/> and www.YouTube.com/statedept<')
        self.remove_by_texts('https://www.youtube.com/user/statevideo<https://www.youtube.com/user/statevideo>')
        self.remove_by_texts('Please click here<https://mcas-proxyweb.mcas.ms/certificate-checker?login=false&originalUrl=https%3A%2F%2Fwww.state.gov.mcas.ms%2Fsecretary-blinkens-participation-in-the-second-summit-for-democracy%2F%3FMcasTsid%3D20893&McasCSRF=f00e87df08f16dddb6b168754be5371a57be6eb48faa37e4a2d0e50005dffb45> for more information on Secretary Blinken’s participation in the Summit for Democracy.')
        self.remove_by_texts('Preset and final access time')
        self.remove_by_texts('No Department Briefing')
        self.remove_by_texts('homepage<https://www.state.gov/>and Youtube channel')
        self.remove_by_texts('www.state.gov/climatesummit<http://www.state.gov/climatesummit>')
        self.remove_by_texts('www.state.gov<http://www.state.gov>')
        self.remove_by_texts('www.state.gov.<https://www.state.gov/>')
        self.remove_by_texts('www.state.gov<http://www.state.gov/>andwww.YouTube.com>')
        self.remove_by_texts('www.state.gov<http://www.state.gov/>andwww.YouTube.com')
        self.remove_by_texts('www.YouTube.com/statedept<https:')
        self.remove_by_texts('www.YouTube.com/statedept<https')
        self.remove_by_texts('www.youtube.com/statedept')
        self.remove_by_texts('www.YouTube.com/statedept')
        self.remove_by_texts('www.Youtube.com/statedept')
        self.remove_by_texts('https://www.state.gov/summit-for-democracy-2023/<https://www.state.gov/summit-for-democracy-2023/')
        self.remove_by_exact_texts('Secretary Blinken follows President Biden’s schedule.')
        self.remove_by_exact_texts('Secretary Blinken follows President Biden’s schedule in New York City, New York.')
        self.remove_by_exact_texts('Secretary Blinken follows President Biden’s schedule in the afternoon.')
        self.remove_by_exact_texts('Secretary Blinken attends Chief of Mission Conference events throughout the day at the Department of State.')
        self.remove_by_texts('Final access time for')
        self.remove_by_texts('Final access')
        self.remove_by_exact_texts('Acting Assistant Secretary for European and Eurasian Affairs Philip T. Reeker')
        self.remove_by_exact_texts('ACTING ASSISTANT SECRETARY FOR European and Eurasian Affairs Philip T. Reeker')
        self.remove_by_exact_texts('.')
        self.remove_by_exact_texts('This page may have been moved, deleted, or is otherwise unavailable. To help you find what you are looking for:')
        self.remove_by_texts('streamed live')
        self.remove_by_texts('attends meetings and briefing')
        self.remove_by_exact_texts('ACTING ASSISTANT SECRETARY for European and Eurasian Affairs Philip T. Reeker')
        self.remove_by_texts('Pre-set time')
        self.remove_by_exact_texts('Special Presidential Envoy for Climate John Kerry')
        self.remove_nan()
        self.fixtext('LOCALS','LOCAL S')
        self.fixtext('.m.D','.m. D')
        self.remove_by_texts('be livestreamed')
        
        self.add_links()
        self.fix_orphan_links()
        print('links cleaned')
        
        self.fixtext('SecretaryBlinken','Secretary Blinken ')
        self.fixtext(' ison ',' is on ')
        self.fixtext(' withMoldovan ',' with Moldovan ')
        self.fixtext(' AustralianForeign ',' Australian Foreign ')
        self.fixtext(' avirtualroundtable ',' a virtual round table ')
        self.fixtext('m.S','m. S')
        self.fixtext('withBruneian','with Bruneian')
        self.fixtext('Blinkenmeets','Blinken meets')
        self.fixtext('withIcelandic PresidentGudni','with Icelandic President Gudni')
        self.fixtext('withJapanese','with Japanese')
        self.fixtext('.m.Acting','.m. Acting')
        self.fixtext('ActingAssistant','Acting Assistant')
        self.fixtext('m.A','m. A')
        self.fixtext('m.L','m. L')
        self.fixtext('m.U','m. U')
        self.fixtext('SecretaryReeker','Secretary Reeker')
        self.fixtext('lunchwith','lunch with')
        self.fixtext('meetwith','meet with')
        self.fixtext('meetswith','meets with')
        self.fixtext('andCanadian','and Canadian')
        self.fixtext('Donfriedmeets','Donfried meets')
        self.fixtext('Nulandmeets','Nuland meets')
        self.remove_by_texts('meetings and briefings')
        self.remove_by_texts('Send us a message using ourcontact us form')
        self.remove_by_texts('live-streamed')
        self.remove_by_texts('usaid.gov<https://gcc02.safelinks.protection.ou')
        
        self.remove_duplicates()
        
        self.add_link_col()
        print('links col added')
        
        self.remove_links()
        self.remove_by_texts('https')
        self.remove_nan()
        self.fixtext('  ',' ')
        self.fixtext('Please click here for more information.','')
        self.fixtext('Please clickhere for more information.','')
        self.fixtext('Please click here for more information','')
        self.fixtext('Pleas click here for more information.','')
        self.fixtext('Click here for more information.','')
        self.fixtext('Pleas clickhere for more information.','')
        self.fixtext('clickhere for more information.','')
        self.fixtext('Please clickhere for more information.','')
        self.fixtext('Please click see the Secretary’s trip page for more information.','')
        self.fixtext('Please click here for moreinformation.','')
        self.fixtext('Please click here for moreinformation.','')
        self.fixtext('Please click here or more information.','')
        self.fixtext('Please clickhere for information.','')
        self.fixtext('Please clickhere for information','')
        self.fixtext('Please click here and here for more information.','')
        self.fixtext('Please click here for the Anchorage part of the trip.','')
        self.fixtext('Please clickhere formore information.','')
        self.fixtext('Please click','')
        self.fixtext('Please see the announcement for more information.','')
        self.fixtext('Please view the trip announcement for more information.','')
        self.fixtext('Please see the announcement  for more information.','')
        self.fixtext('Pleasesee the Secretary’s trip page for more information.','')
        self.fixtext('Please see the Deputy Secretary’s trip page for more information.','')
        self.fixtext('Pleaseview the statement announcing Secretary Blinken’s travel for more information.','')
        self.fixtext('Please view the Notice to the Press for more information.','')
        self.fixtext('Please see the Secretary’s trip page for more information.','')
        self.fixtext('Please view the statement announcing Secretary Blinken’s travel for more information.','')
        self.fixtext('Please read the announcement  for more information.','')
        self.fixtext('July26','July 26')
        self.remove_duplicates()
        
        self.fixtext('UNDER SECRETARY FOR ARMS CONTROL AND INTERNATIONAL SECURITY BONNIE D. JENKINS','')
        self.fixtext('(CLOSED PRESS COVERAGE)','')
        self.fixtext('withEU','with EU')
        self.fixtext('London,Brussels,','London, Brussels,')
        self.fixtext('AmbassadorBernicatvirtually','Ambassador Bernicat virtually')
        
        
        self.fixtext('Austinmeet','Austin meet')
        self.fixtext('Forum:Business','Forum: Business')
        
        self.fixtext('Canada,from','Canada, from')
        self.fixtext('Reekerattends','Reeker attends')
        self.fixtext('Reekerparticipates','Reeker participates')
        self.fixtext('withFrenchAmbassadorto','with French Ambassador to')
        
        self.fixtext('StatesPhilippe','States Philippe')
        self.fixtext('AtlantischeGesellschaft','Atlantische Gesellschaft')
        self.fixtext('withTurkishAmbassadorto','with Turkish Ambassadorto')
        self.fixtext('StatesSerdarKilic','States Serdar Kilic')
        self.fixtext('theWorld','the World')
        self.fixtext('theOcean','the Ocean')
        
        self.fixtext('withCCP','with CCP')
        self.fixtext('andDhakaApril','and Dhaka April')
        self.fixtext('toBeirut','to Beirut')
        self.fixtext('Framework+UK','Framework + UK')
        self.fixtext('Center,from','Center, from')
        self.fixtext('NairobiEmployees','Nairobi Employees')
        self.fixtext('Members,from','Members, from')
        self.fixtext('AssistantSecretary','Assistant Secretary')
        self.fixtext('CopenhagenMeet','Copenhagen Meet')
        self.fixtext('aU.S','a U.S')
        self.fixtext('JeppeKofod','Jeppe Kofod')
        self.fixtext('PeleBroberg','Pele Broberg')
        self.fixtext('','') 
        self.fixtext('CultureJenisav','Culture Jenisav')
        self.fixtext('theHellisheidi','the Hellisheidi')
        self.fixtext('Th.Johannesson','Th. Johannesson')
        self.fixtext('inReykjavik','in Reykjavik')
        self.fixtext('ThorThordarson','Thor Thordarson')
        self.fixtext('MinisterGudlaugur','Minister Gudlaugur')
        self.fixtext('withIcelandic','with Icelandic')
        self.fixtext('IsraeliLeader','Israeli Leader')
        self.fixtext('IsraeliAlternate','Israeli Alternate')       
        self.fixtext('theDepartment','the Department')
        self.fixtext('p.mDeputy','p.m. Deputy')
        self.fixtext('andRefugee','and Refugee')
        self.fixtext('avirtualministerialmeetingwithkey partnersonAfghanistan','a virtual ministerial meeting with key partners on Afghanistan')
        self.fixtext('thePalace','the Palace')
        self.fixtext('withDutch','with Dutch')
        self.fixtext('Medinameets','Medina meets')
        self.fixtext('withHis','with His')
        self.fixtext('Medinais','Medina is')
        self.fixtext('Shermanmeets','Sherman meets')
        self.fixtext('totheUAE,theUnitedKingdom,Israel','to the UAE, the United Kingdom, Israel')
        self.fixtext('thesustainability','the sustainability')
        self.fixtext('withUkrainian','with Ukrainian')
        self.fixtext('MinisterAnnalena','Minister Annalena')
        self.fixtext('andUK Ministerof StateforMiddle East,North Africaand North AmericaJames Cleverlyin','and UK Ministerof State for Middle East, North Africa and North America James Cleverly in')
        self.fixtext('ForeignMinisterIgnazio','Foreign Minister Ignazio')
        self.fixtext('SergeyLavrov','Sergey Lavrov')
        self.fixtext('MinisterMarise','Minister Marise')
        self.fixtext('JapaneseForeign MinisterYoshimasa','Japanese Foreign Minister Yoshimasa')
        self.fixtext('Jaishankarin','Jaishankar in')
        self.fixtext('MinisterYoshimasa','Minister Yoshimasa')
        self.fixtext('AustralianPrime','Australian Prime')
        self.fixtext('Leadershipin','Leadership in')
        self.fixtext('(POOLED CAMERA SPRAY AT BOTTOM)','')
        self.fixtext('(POOLED CAMERA SPRAY AT TOP)','')
        self.fixtext('BureauJakub','Bureau Jakub')
        self.fixtext('SecretaryNulandattends','Secretary Nuland attends')
        self.fixtext('ofthe','of the')
        self.fixtext('Japan,in','Japan, in')
        self.fixtext('withIndian','with Indian')
        self.fixtext('fromMarch','from March')
        self.fixtext('fromApril','from April')
        self.fixtext('JacquesPittloudand','Jacques Pittloud and')
        self.fixtext('StatesOksanaMarkarovaat','States Oksana Markarova at')
        self.fixtext('withChinese','with Chinese')
        self.fixtext('withThai ','with Thai')
        self.fixtext('toFijifromJuly','to Fiji from July')
        self.fixtext('withIsraeli Prime MinisterYair Lapid inJerusalem','with Israeli Prime Minister Yair Lapid in Jerusalem')
        self.fixtext('withPhilippine','with Philippine')
        self.fixtext(' ina ',' i na ')
        self.fixtext(' fairand ',' fair and ')
        self.fixtext('byDemocratic','by Democratic')
        self.fixtext('Tshisekediin','Tshisekedi in')
        self.fixtext('inKinshasa','in Kinshasa')
        self.fixtext('MinisterChristophe','Minister Christophe')
        self.fixtext('KoreaAmbassadorto','Korea Ambassador to')
        self.fixtext('meetingwithAfrican','meeting with African')
        self.fixtext('AlumniinWashington','Alumni in Washington')
        self.fixtext('toFlorida andSweden','to Florida and Sweden')
        self.fixtext('fromSeptember','from September')
        self.fixtext('McAuliffeattend','McAuliffe attend')
        self.fixtext('andSpecial','and Special')
        self.fixtext('forCounterterrorismTim','for Counterterrorism Tim')
        self.fixtext('Betts,Special','Betts, Special')
        self.fixtext('Noyes,Acting','Noyes, Acting')
        self.fixtext('Popu`lation,','Population,')
        self.fixtext('Pyatt,Assistant','Pyatt, Assistant')
        self.fixtext('Leaf,Assistant','Leaf, Assistant')
        self.fixtext('Kritenbrink,Assistant','Kritenbrink, Assistant')
        self.fixtext('Phee,Assistant','Phee, Assistant')
        self.fixtext('forEuropeanand','for European and')
        self.fixtext('Allen,Assistant','Allen, Assistant')
        self.fixtext('Zeya,Under','Zeya, Under')
        self.fixtext('Sherman,Counselor','Sherman, Counselor')    
        self.fixtext('McKeonattends','McKeon attends')    
        self.fixtext('defendersfrom','defenders from')    
        self.fixtext('ServiceSecretary','Service Secretary')    
        self.fixtext('CrimeExecutive','Crime Executive')    
        self.fixtext('NationsOffice','Nations Office')    
        self.fixtext('forDefenseRichard','for Defense Richard')    
        self.fixtext('DefenseSecretary','Defense Secretary')    
        self.fixtext('MahmoudAbbasin','Mahmoud Abbasin') 
        self.fixtext(' Yiin ','Yi in') 
        self.fixtext('TradeandTechnology','Trade and Technology')
        
        self.fixtext('(OPEN PRESS COVERAGE)','')
        self.fixtext('UKMinistero','UK Ministero')
        self.fixtext('Reekerhaslunch','Reeker has lunch')
        self.fixtext('Donfriedattends','Donfried attends')
        self.fixtext('Donfrieddelivers','Donfried delivers')
        self.fixtext('(POOLED PRESS COVERAGE)','')
        self.fixtext('SecretaryNoyesis','Secretary Noyes is')
        self.fixtext('Fernández','Fernandez')
        self.fixtext('Nulandis','Nuland is')
        self.remove_by_texts('Department of State is closed')
        self.remove_by_texts('telephonic press')
        
        self.remove_duplicates()
        self.fixtext('Central Asian Affairs Donald Lu','Central Asian Affairs Donald Lu ')
        self.fixtext('LOCAL Secretary participates in a G7 Family Photo, in London, United Kingdom.','LOCAL Secretary Blinken participates in a G7 Family Photo, in London, United Kingdom. ')
        self.fixtext('(MEDIA DETERMINED BY HOST)','')
        self.fixtext('Fernandezdelivers','Fernandez delivers')
        self.add_names_col()
        print('name col added')
        
        self.fixdate('Public Schedule-','')
        self.fixdate(' here for more information','')
        self.fixdate('here for more information','')
        self.fixdate('see the announcement for more information.','')
        self.fixdate('the announcement for more information.','')
        self.fixdate('Public Schedule ','')
        self.fixdate('Daily ','')
        self.fixdate(' (Updated)','')
        self.fixdate('th,',',')
        self.fixdate(' May','May')
        self.fixdate(' June','June')
        self.fixdate(' Sept','Sept')
        self.fixdate('January 20 2022','January 20, 2022')
        self.fixdate('June 30,2021','June 30, 2021')
        self.remove_by_exact_texts('the announcement for more information.')
        self.remove_by_exact_texts('Assistant Secretary for South and Central Asian Affairs Donald Lu')
        self.remove_by_exact_texts('')
        self.remove_by_exact_texts('Assistant Secretary for South and Central Asian Affairs Donald Lu')
        
        
        self.remove_nan()
        self.convertdate()
        self.add_titles_col()
        self.add_ranks_col()
        self.remove_duplicates()
        self.add_counts()
        self.add_travel_meet_kind()
        self.add_travel_info()
        self.add_countries_involved()
        self.add_accom()
        self.add_topics_orgs()

        print('other col added')
        self.save()
        self.FINALIZE()
        print('Done!')

    '''
    --------------6.最终生成工具---------------
    6.1 when_who_where_what_travel 返回出访相关表格
    6.2 strangers 返回外交活动中非美人员
    6.3 when_who_where_what_meet 返回会面相关表格

    '''
    
    def when_who_where_what_travel(self):
        
        '''
        返回出访相关表格
              iDcN 行为日期，列为外交官名字，内容为出访国家的表
              iDcC 行为日期，列为出访国家，内容为外交官名字的表
              iDcR 行为日期，列为出访国家，内容为外交官级别的表（5为总统最高）
              iCcN 行为出访国家，列为外交官名字，内容为出访总数的表
              iCcT 行为出访国家，列为主题，内容为频率的表
              iNcT 行为外交官名字，列为主题，内容为频率的表
              iCcO 行为出访国家，列为机构，内容为频率的表
              iNcO 行为出访国家，列为机构，内容为频率的表
         '''
        
        maxs=max(self.current.dates)+timedelta(days=1)
        mins=min(self.current.dates)-timedelta(days=1)
        indt=list(pd.date_range(mins,maxs))
        names=list(self.names)+['Biden'] 
        topics=[]
        for top in self.current.topics:
            if type(top)!=float:
                topics=topics+list(top.split(';;')[1:])
        topics=list(set(topics))
  
        orgs=[]
        for org in self.current.orgs:
            if type(org)!=float:
                orgs=orgs+list(org.split(';;')[1:])
        orgs=list(set(orgs))
        
        countries=[]
        for c in self.current.countries_inv:
            cc=c.split(';;')[1:]
            cc=['Domestic' if x=='United States' else x for x in cc]
            countries=countries+cc
        countries=list(set(countries))

        for j in range(len(names)):
            names[j]=names[j].strip()
        box=np.empty((len(indt),len(names)),dtype='<U400')
        box2=np.empty((len(indt),len(countries)),dtype='<U400')
        box3=np.zeros((len(countries),len(names)))
        box4=np.zeros((len(countries),len(topics)))
        box5=np.zeros((len(names),len(topics)))
        box6=np.zeros((len(countries),len(orgs)))
        box7=np.zeros((len(names),len(orgs)))
        box8=np.zeros((len(indt),len(countries)))
        box8[:]=None
        
        df=self.current[self.current.travel_kind==1]
        for i in df.index:
            bdate=df.travel_beg[i]+timedelta(days=1)
            edate=df.travel_end[i]
            ns=[df.lastnames[i]]
            nss=df.lastnames[i]
            if type(self.current.accompanies[i])==float:
                ns=ns
            else:
                ns=ns+list(self.current.accompanies[i].split(';;')[1:-1])
                nss=nss+self.current.accompanies[i]
            locs=df.countries_inv[i]
            locsl=locs.split(';;')[1:]
            ranks=[]
            for n in ns:
                box[indt.index(bdate):indt.index(edate),names.index(n)]=locs
                if n!='Biden':
                    ranks.append(6-self.ranks[n])
                else:
                    ranks.append(1)
                for l in locsl:
                    if l=='United States':
                        l='Domestic'
                    box3[countries.index(l),names.index(n)]=box3[countries.index(l),names.index(n)]+(edate-bdate).days
            ranks=max(ranks)
            for l in locsl:
                if l=='United States':
                    l='Domestic'
                box2[indt.index(bdate):indt.index(edate),countries.index(l)]=nss
                box8[indt.index(bdate):indt.index(edate),countries.index(l)]=ranks
            tps=df.topics[i]
            if type(tps)!=float:
                tps=tps.split(';;')[1:]
                for tp in tps:
                    for l in locsl:
                        if l=='United States':
                            l='Domestic'
                        box4[countries.index(l),topics.index(tp)]=box4[countries.index(l),topics.index(tp)]+1
                    for n in ns:
                        box5[names.index(n),topics.index(tp)]=box5[names.index(n),topics.index(tp)]+1
            og=df.orgs[i]
            if type(og)!=float:
                og=og.split(';;')[1:]
                for g in og:
                    for l in locsl:
                        if l=='United States':
                            l='Domestic'
                        box6[countries.index(l),orgs.index(g)]=box6[countries.index(l),orgs.index(g)]+1
                    for n in ns:
                        box7[names.index(n),orgs.index(g)]=box7[names.index(n),orgs.index(g)]+1

        iDcN=pd.DataFrame(box,index=indt,columns=names)
        iDcC=pd.DataFrame(box2,index=indt,columns=countries)
        iDcR=pd.DataFrame(box8,index=indt,columns=countries)
        iCcN=pd.DataFrame(box3,index=countries,columns=names)
        iCcT=pd.DataFrame(box4,index=countries,columns=topics)
        iNcT=pd.DataFrame(box5,index=names,columns=topics)
        iCcO=pd.DataFrame(box6,index=countries,columns=orgs)
        iNcO=pd.DataFrame(box7,index=names,columns=orgs)
        
        iDcN.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_DATE_columns_Names_cell_Countries'+'.xlsx')
        iDcC.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_DATE_columns_Countries_cell_Names'+'.xlsx')
        iDcR.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_DATE_columns_Countries_cell_Ranks'+'.xlsx')
        iCcN.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Countries_columns_Names_cell_Days'+'.xlsx')
        iCcT.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Countries_columns_Topics_cell_Counts'+'.xlsx')
        iNcT.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Names_columns_Topics_cell_Counts'+'.xlsx')
        iCcO.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Countries_columns_Orgs_cell_Counts'+'.xlsx')
        iNcO.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'travels_index_Names_columns_Orgs_cell_Counts'+'.xlsx')
        
        self.iDcN=iDcN
        self.iDcC=iDcC
        self.iCcN=iCcN
        self.iDcR=iDcR
        self.iCcT=iCcT
        self.iNcT=iNcT
        self.iCcO=iCcO
        self.iNcO=iNcO
    
    #不是很好用
    def strangers(self):
        nlp = spacy.load('en_core_web_sm')
        stranger=[]
        for i,t in enumerate(self.current.text):
            doc = nlp(t)
            for ent in doc.ents:
                if ent.label_== 'PERSON':
                    box=''
                    if ent.text not in self.names and ent.text!='LOCAL'and ent.text!='Biden'and ent.text!='Official Allen':
                        box=box+';;'+str(ent.text)                        
            stranger.append(box)
        c=self.current.copy()
        c['Others']=stranger
        c.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'with_others.xlsx')
        
    #未完成
    def when_who_where_what_meet(self):
        
        'returns a df with countries as indexs and date as columns, diplomats in each cell'
        
        maxs=max(self.current.dates)+timedelta(days=1)
        mins=min(self.current.dates)-timedelta(days=1)
        indt=list(pd.date_range(mins,maxs))
        names=list(self.names)+['Biden'] 
        topics=[]
        for top in self.current.topics:
            if type(top)!=float:
                topics=topics+list(top.split(';;')[1:])
        topics=list(set(topics))
  
        orgs=[]
        for org in self.current.orgs:
            if type(org)!=float:
                orgs=orgs+list(org.split(';;')[1:])
        orgs=list(set(orgs))
        
        countries=[]
        for c in self.current.countries_inv:
            cc=c.split(';;')[1:]
            cc=['Domestic' if x=='United States' else x for x in cc]
            countries=countries+cc
        countries=list(set(countries))

        for j in range(len(names)):
            names[j]=names[j].strip()
        box=np.empty((len(indt),len(names)),dtype='<U400')
        box2=np.empty((len(indt),len(countries)),dtype='<U400')
        box3=np.zeros((len(countries),len(names)))
        box4=np.zeros((len(countries),len(topics)))
        box5=np.zeros((len(names),len(topics)))
        box6=np.zeros((len(countries),len(orgs)))
        box7=np.zeros((len(names),len(orgs)))

        df=self.current[self.current.meet_kind==1]
        for i in df.index:
            date=df.dates[i]
            ns=[df.lastnames[i]]
            nss=df.lastnames[i]
            if type(self.current.accompanies[i])==float:
                ns=ns
            else:
                ns=ns+list(self.current.accompanies[i].split(';;')[1:-1])
                nss=nss+self.current.accompanies[i]
            locs=df.countries_inv[i]
            locsl=locs.split(';;')[1:]
            for n in ns:
                box[indt.index(date),names.index(n)]=locs
                for l in locsl:
                    if l=='United States':
                        l='Domestic'
                    box3[countries.index(l),names.index(n)]=box3[countries.index(l),names.index(n)]+1
            for l in locsl:
                if l=='United States':
                    l='Domestic'
                box2[indt.index(date),countries.index(l)]=nss
            tps=df.topics[i]
            if type(tps)!=float:
                tps=tps.split(';;')[1:]
                for tp in tps:
                    for l in locsl:
                        if l=='United States':
                            l='Domestic'
                        box4[countries.index(l),topics.index(tp)]=box4[countries.index(l),topics.index(tp)]+1
                    for n in ns:
                        box5[names.index(n),topics.index(tp)]=box5[names.index(n),topics.index(tp)]+1
            og=df.orgs[i]
            if type(og)!=float:
                og=og.split(';;')[1:]
                for g in og:
                    for l in locsl:
                        if l=='United States':
                            l='Domestic'
                        box6[countries.index(l),orgs.index(g)]=box6[countries.index(l),orgs.index(g)]+1
                    for n in ns:
                        box7[names.index(n),orgs.index(g)]=box7[names.index(n),orgs.index(g)]+1

        MiDcN=pd.DataFrame(box,index=indt,columns=names)
        MiDcC=pd.DataFrame(box2,index=indt,columns=countries)
        MiCcN=pd.DataFrame(box3,index=countries,columns=names)
        MiCcT=pd.DataFrame(box4,index=countries,columns=topics)
        MiNcT=pd.DataFrame(box5,index=names,columns=topics)
        MiCcO=pd.DataFrame(box6,index=countries,columns=orgs)
        MiNcO=pd.DataFrame(box7,index=names,columns=orgs)
        
        MiDcN.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_DATE_columns_Names_cell_Countries'+'.xlsx')
        MiDcC.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_DATE_columns_Countries_cell_Names'+'.xlsx')
        MiCcN.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_Countries_columns_Names_cell_Days'+'.xlsx')
        MiCcT.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_Countries_columns_Topics_cell_Counts'+'.xlsx')
        MiNcT.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_Names_columns_Topics_cell_Counts'+'.xlsx')
        MiCcO.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_Countries_columns_Orgs_cell_Counts'+'.xlsx')
        MiNcO.to_excel('Analysis/'+self.president+'/'+self.president+'_'+'meetings_index_Names_columns_Orgs_cell_Counts'+'.xlsx')
 
        self.MiDcN=MiDcN
        self.MiDcC=MiDcC
        self.MiCcN=MiCcN
        self.MiCcT=MiCcT
        self.MiNcT=MiNcT
        self.MiCcO=MiCcO
        self.MiNcO=MiNcO

