__author__ = 'adb'


with open('seprox', 'r') as f:
    i = 1
    d = {}
    for line in f:
        line = line.strip()
        timestamp, v1, v2 = line.split('\t', 2)
        d[timestamp] = i
        i+=1

