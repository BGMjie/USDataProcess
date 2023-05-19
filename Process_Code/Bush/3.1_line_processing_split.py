output_file = open('bush_split.txt', 'w+', encoding='utf8')
for line1 in open('bush_html_new.txt', 'r', encoding='utf8'):
    date = line1.split('\t')[0]
    str_all = line1.split('\t')[1]
    para = str_all.split(';;;;')
    for line in para:
        line = line.strip()
        output_str = date + '\t' + line + '\n'
        output_file.write(output_str)
output_file.close()