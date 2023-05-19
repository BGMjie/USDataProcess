import pandas as pd
bush_clean = pd.read_csv('bush_clean.csv', encoding = 'utf8')

def line_transform(inputs):
    dates = []
    name = []
    texts = [' ']
    name_upper = 'START'
    for i, line in enumerate(inputs.Texts):
        if line.isupper():
            name_upper = line.upper()
        else:
            texts[-1] = texts[-1] + ' ' + line
        try:
            texts.append(line)
            dates.append(inputs.Dates[i])
            name.append(name_upper)
        except:
            pass
    form = pd.DataFrame(dates, columns=['Dates'])
    form['Name'] = name
    form['Texts'] = texts[1:]
    return form

T = line_transform(bush_clean)
T.to_csv('Bush_Transform.csv')





# def line_transform(input):
#     str = input.split('\t')
#     para = []
#     str_temp = ''
#     original_upper = True
#     for line in str[1]:
#         new_upper = line.isupper()
#         if original_upper and new_upper:
#             pass
#         if original_upper and not new_upper:
#             str_temp = str_temp + ';;' + line
#         if not original_upper and new_upper:
#             para.append(str_temp)
#             str_temp = ''
#         if not original_upper and not new_upper:
#             str_temp = str_temp + ';;' + line
#         if new_upper:
#             str_temp = line + ';;'
#         else:
#             pass
#         original_upper = new_upper
#     return para

# output_file =open('bush_transform.txt', 'w+', encoding='utf8')

# str_temp = ''
# para = []
# original_upper = True
# for line in enumerate(texts):
#
#     new_upper = str(line).isupper()
#     if original_upper and new_upper:
#         pass
#     if original_upper and not new_upper:
#         str_temp = str_temp + ';;' + line
#         # str_temp.append(line)
#     if not original_upper and new_upper:
#         para.append(str_temp)
#         str_temp = ''
#     if not original_upper and not new_upper:
#         # str_temp = str_temp + ';;' + line
#     if new_upper:
#         str_temp = line + ';;'
#     else:
#         pass
#     original_upper = new_upper
#     para.append(str_temp)
# print(para)





# for line in open('bush_split.txt', 'r', encoding='utf8'):
#     date = line.split('\t')[0]
#     texts = line_transform(line)
#     for t in texts:
#         output_str = date + '\t' + t + '\n'
#         output_file.write(output_str)
# output_file.close()