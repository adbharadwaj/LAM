#!/usr/bin/env python
# a stacked bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt




def plot_ucs_size_composition_vs_ssd_cutoff(threeUC, fourUC, fiveUC):
    N = 6

    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, threeUC, width, color='r')
    p2 = plt.bar(ind, fourUC, width, color='y', bottom=threeUC)
    p3 = plt.bar(ind, fiveUC, width, color='g', bottom=[i+j for i,j in zip(threeUC, fourUC)])

    plt.ylabel('#UCs')
    plt.title('Hyperedge Composition')
    plt.xticks(ind + width/2., ('0.1', '0.2', '0.3', '0.4', '0.5', '0.6'))
    plt.yticks(np.arange(0, 81, 10))
    plt.legend((p1[0], p2[0], p3[0]), ('UCs of size 3', 'UCs of size 4', 'UCs of size 5'))

    plt.show()


threeUC = (20, 35, 30, 35, 27, 34)
fourUC = (25, 32, 34, 20, 25, 12)
fiveUC = (5, 2, 4, 2, 2, 0)
plot_ucs_size_composition_vs_ssd_cutoff(threeUC, fourUC, fiveUC)