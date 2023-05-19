import pandas as pd
bush_transform = pd.read_csv('Bush_Transform.csv', encoding='utf8')
dates = bush_transform.iloc[:, 1]
name = bush_transform.iloc[:, 2]
texts = bush_transform.iloc[:, 3]

def line_delete(text):
    delete_or_not = 0
    people_list = ['SECRETARY OF STATE RICE',
                   'DEPUTY SECRETARY OF STATE NEGROPONTE',
                   'DEPUTY SECRETARY OF STATE ZOELLICK',
                   'UNDER SECRETARY OF STATE FOR POLITICAL AFFAIRS BURNS',
                   'ASSISTANT SECRETARY OF STATE FOR EDUCATIONAL AND CULTURAL AFFAIRS POWELL',
                   'SECRETARY OF STATE POWELL',
                   'DEPUTY SECRETARY OF STATE ARMITAGE',
                   'UNDER SECRETARY OF STATE JOHN R. BOLTON',
                   ]
    for people_name in people_list:
        if people_name in str(text):
            delete_or_not += 1
    return delete_or_not

T = pd.DataFrame()
delete_or_not = []
T['Dates'] = dates
T['Name'] = name
T['Texts'] = texts
for line in T['Texts'].tolist():
    delete_or_not.append(line_delete(line))
T['Delete_or_not'] = delete_or_not
T = T.drop(T[T.Delete_or_not > 0].index)
T.to_csv('Bush_Transform_new.csv', encoding='utf8')