__author__ = 'adb'


am_file = 'am-ssd-0.6.txt'
lam_file = 'lam-ssd-0.6.txt'
am_tuples = ""
lam_tuples = ""

with open(am_file, 'r') as f:
    for line in f:
        if line.startswith('('):
            am_tuples += line + ';'

with open(lam_file, 'r') as f:
    for line in f:
        if line.startswith('('):
            if line in am_tuples:
                am_tuples.replace(line+';', '')
            else:
                lam_tuples += line + ';'

x = lam_tuples.split(';')
for i in x:
    print(i)