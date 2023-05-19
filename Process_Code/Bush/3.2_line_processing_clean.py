import pandas as pd

def save_line(text):
    action_list = ['a.m.', 'p.m.']
    people_list = ['SECRETARY OF STATE RICE',
                   'DEPUTY SECRETARY OF STATE NEGROPONTE',
                   'DEPUTY SECRETARY OF STATE ZOELLICK',
                   'UNDER SECRETARY OF STATE FOR POLITICAL AFFAIRS BURNS',
                   'ASSISTANT SECRETARY OF STATE FOR EDUCATIONAL AND CULTURAL AFFAIRS POWELL',
                   'SECRETARY OF STATE POWELL',
                   'DEPUTY SECRETARY OF STATE ARMITAGE',
                   'UNDER SECRETARY OF STATE JOHN R. BOLTON',
                   ]
    find_action_or_not = 0
    find_people_or_not = 0
    for action in action_list:
        if action in str(text):
            find_action_or_not += 1
    for people in people_list:
        if people in str(text):
            find_people_or_not += 1
    saveline = find_people_or_not + find_action_or_not
    return saveline

def drop_line(text):
    drop_list = ['camera',
                 'cameras'
                 'Camera',
                 'press',
                 'Press',
                 'Stills',
                 'stills',
                 'writers',
                 'Final access time']
    drop_or_not = 0
    for drop_word in drop_list:
        if drop_word in str(text):
            drop_or_not += 1
    return drop_or_not

bush_split = pd.read_csv('bush_split.csv', encoding='utf8')
date = bush_split.iloc[:, 0]
texts = bush_split.iloc[:, 1]
T = pd.DataFrame()
T['Dates'] = date
T['Texts'] = texts
save_or_not = []
drop_or_not = []
for text in T['Texts'].tolist():
    save_or_not.append(save_line(text))
    drop_or_not.append(drop_line(text))
T['Save_or_not'] = save_or_not
T['Drop_or_not'] = drop_or_not
T = T.drop(T[T.Save_or_not < 1].index)
T = T.drop(T[T.Drop_or_not > 0].index)
T.to_csv('bush_clean.csv', encoding='utf8')