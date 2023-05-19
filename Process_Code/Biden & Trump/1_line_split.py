
output_file = open('biden_split.txt', 'w+', encoding='utf8')
for line1 in open('biden_output.txt', 'r', encoding='utf8'):
    date = line1.split('\t')[0]
    str_all = line1.split('\t')[1]
    para = str_all.split(';;;;')
    for line in para:
        line = line.strip()
        output_str = date + '\t' + line + '\n'
        output_file.write(output_str)
output_file.close()


import numpy as np
import pandas as pd
import re
#
# biden_line = pd.read_csv('biden_line_new.csv', index_col=0)
# texts = biden_line.iloc[:, 1]
# dates = biden_line.iloc[:, 0]
# biden_line.index = np.arange(len(biden_line))
# trump_line = pd.read_csv('trump_line_new.csv', index_col=0)
# trump_line.index = np.arange(len(trump_line))

def line_transform(inputs):
    dates = []
    CAPS = []
    texts = []
    for i, line in enumerate(inputs):
        if 'No Department Press Briefing' in line or 'Department Press Briefing' in line or 'No Briefing' in line or 'No Department Briefing' in line or 'NoDepartment Press Briefing' in line or 'No Department press briefing' in line:
            pass
        else:
            # 如果line是大写的就用CAP变量记下来，后面的lower case都是关于CAP的
            if line.isupper():
                CAP = line
            else:
                # 这一段是处理超连接的，如果有超连接就把它接到上一个lower case text去
                # 超链接不全，用'here<https://www'查找
                if '<' in line and '>' in line and 'www.state.gov<http://www.state.gov/>.' in line or '2017-2021.state.gov<http://2017-2021.state.gov/>.' in line or 'www.youtube.com/statedept' in line.lower() or 'www.state.gov<http://www.state.gov>' in line or 'http://www.youtube.com/statedept' in line.lower() or 'here<https://www.state.gov/' in line:
                    try:
                        texts[-1] = texts[-1] + ' ' + line
                        pass
                    except:
                        pass
                else:
                    # 如果line是lower case text，记录一行date，cap，text
                    texts.append(line)
                    dates.append(inputs.Dates[i])
                    CAPS.append(CAP)
    form = pd.DataFrame(dates, columns=['Dates'])
    form['CAPS'] = CAPS
    form['Texts'] = texts
    return form
#
#
# # def update():
#     # A = line_transform(trump_line)
#     # A.to_csv('Trump_Transformed_new.csv')
# A = line_transform(biden_line)
# A.to_csv('Biden_Transformed_new.csv')
