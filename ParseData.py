import sys
from Ensemble import Ensemble
import matplotlib.pyplot as plt

__author__ = 'adb'


INPUTFILE = sys.argv[1]
SIGMA = float(sys.argv[2])
CONSTRAINT = sys.argv[3]





with open(INPUTFILE, 'r') as f:
    T = Ensemble()
    for line in f:
        line = line.strip()
        timestamp, v1, v2 = line.split('\t', 2)
        T.add_edge(timestamp, v1, v2)

if CONSTRAINT == 'am':
    T.generate_antimonotone_hyperedges_report(SIGMA)
elif CONSTRAINT == 'lam':
    T.generate_looselyantimonotone_hyperedges_report(SIGMA)
else:
    print(T)
    # plot_variation_in_ssd(T)

