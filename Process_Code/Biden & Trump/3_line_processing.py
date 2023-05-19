import pandas as pd
import numpy as np
import re
trump_line = pd.read_csv('../Data/Mid_data/Trump/trump_2_line_raw.csv')
biden_line = pd.read_csv('../Data/Mid_data/Biden/biden_2_line_raw.csv')


# UPDATE misspelled 'Copper', 'TIllerson','McGurk' and 'Stilwell' are added and Cap and lower case variations in links are included

lowername_trump = ['Barsa', 'Bernicat', 'Biegun', 'Birx', 'Breier', 'Brownback', 'Brownfield', 'Bulatao', 'Chung',
                       'Cooper', 'Copper','Currie', 'Destro', 'Evanoff', 'Fannon', 'Foote', 'Ford', 'Friedt', 'Galt', 'Garber',
                       'Giuda', 'Goldstein', 'Green', 'Greenfield', 'Grunder', 'Guida', 'Hale', 'Haslach', 'Hook',
                       'Hushek', 'Jacobs', 'Jacobson', 'Kaidanow', 'Kozak', 'Krach', 'Lawler', 'Madison',
                       'Markgreen', 'McGuigan', 'Mcgurk','McGurk', 'Mitchell', 'Moley', 'Moore', 'Mull', 'Murphy', 'Nagy',
                       'Natali', 'Nauert', 'O’Connell', 'Palmieri', 'Phee', 'Poblete', 'Pompeo', 'Reeker', 'Risch',
                       'Royce', 'Russel', 'Sales', 'Schenker', 'Shannon', 'Singh', 'Stillwell', 'Stilwell', 'Sullivan', 'Taplin',
                       'Thompson', 'Thornton', 'Tillerson','TIllerson', 'Todd', 'Walsh', 'Wells', 'Wharton', 'Yamamoto', 'Yun']

# UPDATE 'Allen','Price','Patel', and 'Porter' are added and Cap and lower case variations in links are included

lowername_biden = ['Allen','Bernicat', 'Bitter', 'Blinken', 'Chung', 'Cormack', 'Donfried', 'Feltman', 'Fernandez', 'Godfrey',
                   'Hale', 'Hood', 'Jackson', 'Jenkins', 'Kang', 'Kerry', 'Kritenbrink', 'Leaf', 'Lempert', 'Lenderking',
                   'Lewis', 'Lu ', 'Lussenhop', 'Massinga', 'McKeon', 'Medina', 'Murray', 'Nichols', 'Noyes', 'Nuland','Patel',
                   'Peterson', 'Phee','Price', 'Power','Porter', 'Reeker', 'Robinson', 'Satterfield', 'Sherman', 'Sison', 'Smith',
                   'Steele', 'Stewart', 'Thompson', 'Toloui', 'Trudeau', 'Vallsnoyes', 'Walsh', 'Witkowsky', 'Yael',
                   'Zeya', 'Zuniga']


def save_line(text,lowernames):
    # returns how many last names are included, 0 means the str has no relevant name in it.
    save_or_not = 0
    for name in lowernames:
        if name in str(text) or name.lower() in str(text):
            save_or_not += 1
    return save_or_not

def find_lastname(text,lowernames):
    # returns the last names included in str, [] means the str has no relevant name in it.
    lastname = []
    for name in lowernames:
        if name in str(text) or name.lower() in str(text):
            lastname = name
    return lastname

def check_start(text):
    # check if the str has certain start pattern, if True then the str is a seperate link that should be added back to last str
    check_list=['here','Please click here','see the announcement','the announcement','Please clickhere']
    for check_str in check_list:
        if text[:len(check_str)]==check_str:
            return True
        
def find_all(string, sub):
    # a tool function to locate all substrings in a str
    start = 0
    pos = []
    while True:
        start = string.find(sub, start)
        if start == -1:
            return pos
        pos.append(start)
        start += len(sub)
        
def locate_links(text):
    # a tool function to locate all links in a str
    s=find_all(text,'<')
    e=find_all(text,'>')
    if len(s)==1 and len(e)==1:
        link=text[int(s[0]):int(e[0])+1]
        return [link]
    if len(s)>1 and len(e)>1 and len(s)==len(e):
        link=[]
        for i in range(len(s)):
            li=text[int(s[i]):int(e[i])+1]
            link.append(li)
        return link
    else:
        return 'None'
    
def break_links(link):
    # a tool function to break the content part of a link into a list of words
    link=link.replace('<','')
    link=link.replace('>','')
    content=link.split('/')[-2]
    content=content.split('-')
    return content

def compare_text_link(link,text):
    # a tool function to assess the similarity between the content of a link and the content of a string
    links=break_links(link)
    text=text.replace(',',' ')
    text=text.replace('.',' ')
    texts=text.lower().split(' ')
    common=list(set(texts).intersection(links))
    similiarity= len(common)/len(links)
    return similiarity

def remove_click(texts):
    # a tool function to remove links in a str
    replaces=['Please click here> for more information',
              'Please click here for more information',
              'Please clickhere for more information',
              'please click here for more information',
              ' and here for more information',
              'Please click here',
              'Pleas click here',
              'Please clickhere',
              'for more information',
              'Click here',
              'Clickhere',
              'Pleaseclickhere',
              'Pleaseclick here',
              'Please see the announcement',
              'Learn more',
              'for moreinformation',
              'Please read the announcement',
              ]
    for replace_text in replaces:
        texts=texts.replace(replace_text,'')
    texts=texts.replace('. .','.')
    texts=texts.replace('..','.')
    return texts
            
def process_links(texts):
    # a tool function to seperate inks and content in a str
    links=locate_links(texts)
    if links=='None':
        # if no link just return 'None'
        return texts,'None'
    if len(links)==1:
        # if one link seperate inks and content 
        texts=texts.replace(links[0],'')
        texts=remove_click(texts)
        
        return texts,links[0]
    if len(links)==2:
        # if two links seperate inks and content , also chcek if two links are the same
        if links[0] in links[1]:
            texts=texts.replace(links[0],'')
            texts=remove_click(texts)
            return texts,links[0]
        else:
            texts=texts.replace(links[0],'')
            texts=texts.replace(links[1],'')
            texts=remove_click(texts)
            return texts,links
        
def from_to_corrections(text):
    A=re.search(r' to[A-Z]',text)
    if A:
        text=text[0:A.span()[0]]+text[A.span()[0]:A.span()[1]].replace('to','to ')+text[A.span()[1]:]
        
    B=re.search(r' from[A-Z]',text)
    if B:
         text=text[0:B.span()[0]]+text[B.span()[0]:B.span()[1]].replace('from','from ')+text[B.span()[1]:]
        
    else:
        if 'on travel to travel to' in text:
            text=text.replace('on travel to travel to','on travel to')
        if 'ontravelto' in text:
            text=text.replace('ontravelto','on travel to')
        if 'ontravelto' in text:
            text=text.replace('ontravel','on travel')
        if 'travelto' in text:
            text=text.replace('travelto','travel to')
                     
    return text
         
def make_line_final(president):
    # creat line final table
    # first we select the presidency
    if president == 'trump':
        texts = trump_line.iloc[:, 1]
        dates = trump_line.iloc[:, 0]
        lowernames=lowername_trump
        
    if president == 'biden':
        texts = biden_line.iloc[:, 1]
        dates = biden_line.iloc[:, 0]
        lowernames=lowername_biden
    
    save_or_not = [0]
    last_name = [' ']
    dates_new = [' ']
    texts_new = [' ']
    
    for i in range(len(texts)):
        line=texts[i]
        date=dates[i]
        if check_start(line):
            # this part is intended to handle the case where the line is an orphan link. 
            for j in range(1,5):
                if save_line(texts_new[-j],lowernames)>0 and locate_links(texts_new[-j])=='None' and compare_text_link(locate_links(line)[0],texts_new[-j])>0.5:
                    #print(texts_new[-j],'<-->',line)
                    texts_new[-j] = texts_new[-j]+line
                    pass
                # if the line is an orphan link, we go back to previous strings until we find the matching one to add back on.
        else:
            texts_new.append(line)
            dates_new.append(date)
            save_or_not.append(save_line(line,lowernames))
            last_name.append(find_lastname(line,lowernames))
    T=pd.DataFrame(dates_new,columns=['Dates'])
    T['Org_texts']=texts_new
    T['Lastname'] = last_name
    T['Save_or_not'] = save_or_not
    # here we create a new line table
    saved=T.drop(T[T.Save_or_not < 1].index)
    saved.index=np.arange(len(saved))
    
    # here we begain to create a new link_final df table where texts contents and links are seperate
    dates=[]
    last_names=[]
    texts_pure=[]
    link_list=[]
    counts=[]
    for i,text in enumerate(saved.Org_texts):
        text_pure,links=process_links(text)
        
        if links!='None' and len(links)==2 and links[0]!='<':
        # here we deal with the situation where one line has two links 
            dates.append(saved.Dates[i])
            last_names.append(saved.Lastname[i])
            counts.append(saved.Save_or_not[i])
            texts_pure.append(text_pure)
            link_list.append(links[0])
       # by creating a new line with the same text but different link
            dates.append(saved.Dates[i])
            last_names.append(saved.Lastname[i])
            counts.append(saved.Save_or_not[i])
            texts_pure.append(text_pure)
            link_list.append(links[1])
            
        else:
            dates.append(saved.Dates[i])
            last_names.append(saved.Lastname[i])
            counts.append(saved.Save_or_not[i])
            texts_pure.append(text_pure)
            link_list.append(links)
            

    saved=pd.DataFrame(dates,columns=['Dates'])
    saved['Lastnames']=last_names
    saved['Texts']=texts_pure
    saved['Links']=link_list
    saved['Counts']=counts
    saved.index=np.arange(len(saved))
    new_texts=[]    
    
    for i in range(len(saved.index)):
        c=from_to_corrections(saved.iloc[i].Texts)
        new_texts.append(c)
    saved['Texts']=new_texts
        # correct travel related errors
          
  
    dropped=T.drop(T[T.Save_or_not > 0].index)
    dropped.index=np.arange(len(dropped))
    # first return the one that should be saved, then return the ones that are dropped for error checking
    return saved, dropped

    
# make two line_finals
saved,dropped=make_line_final('biden')
saved.to_csv('../Data/Mid_data/Biden/biden_3_line_processed.csv', encoding='utf8')
dropped.to_csv('../Data/Mid_data/Biden/biden_3_line_processed_dropped.csv', encoding='utf8')
saved,dropped=make_line_final('trump')
saved.to_csv('../Data/Mid_data/Trump/trump_3_line_processed.csv', encoding='utf8')
dropped.to_csv('../Data/Mid_data/Trump/trump_3_line_processed_dropped.csv', encoding='utf8')

