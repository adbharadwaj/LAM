import matplotlib.pyplot as plt
import sys

results_dir = sys.argv[1]



def plot_variation_in_ssd_lam():
    with open(results_dir+'/lam/hyperedges-0.0.tsv', 'r') as f:
        ucs = []
        for line in f:
            line = line.strip()
            ucs.append(line.split('\t'))
        ucs = sorted(ucs, key=lambda tup: tup[-1])
    # print(ssds)
    ssds = [uc[-1] for uc in ucs]
    return ssds, range(1, len(ssds) + 1)


def plot_variation_in_ssd_am():
    with open(results_dir+'/am/hyperedges-0.0.tsv', 'r') as f:
        ucs = []
        for line in f:
            line = line.strip()
            ucs.append(line.split('\t'))
        ucs = sorted(ucs, key=lambda tup: tup[-1])
    # print(ssds)
    ssds = [uc[-1] for uc in ucs]
    return ssds, range(1, len(ssds) + 1)


def plot_percentage_nodes_ssd_am():
    with open(results_dir+'/am/hyperedges-0.0.tsv', 'r') as f:
        ucs = []
        for line in f:
            line = line.strip()
            ucs.append(line.split('\t'))
        ucs = sorted(ucs, key=lambda tup: tup[-1])
    ssds = [uc[-1] for uc in ucs]
    nodes = [uc[1:-1] for uc in ucs]
    cummulitive_nodes = []
    for i in range(len(nodes)):
        if i == 0:
            cummulitive_nodes.insert(i, nodes[i])
        else:
            cummulitive_nodes.insert(i, list(set(cummulitive_nodes[i-1]).union(set(nodes[i]))))
    percentage_of_nodes_covered = [float(100*len(cummulitive_nodes[i]))/75 for i in range(len(cummulitive_nodes))]
    return percentage_of_nodes_covered, range(1, len(ssds) + 1)


def plot_percentage_nodes_ssd_lam():
    with open(results_dir+'/lam/hyperedges-0.0.tsv', 'r') as f:
        ucs = []
        for line in f:
            line = line.strip()
            ucs.append(line.split('\t'))
        ucs = sorted(ucs, key=lambda tup: tup[-1])
    ssds = [uc[-1] for uc in ucs]
    nodes = [uc[1:-1] for uc in ucs]
    cummulitive_nodes = []
    for i in range(len(nodes)):
        if i == 0:
            cummulitive_nodes.insert(i, nodes[i])
        else:
            cummulitive_nodes.insert(i, list(set(cummulitive_nodes[i-1]).union(set(nodes[i]))))
    percentage_of_nodes_covered = [float(100*len(cummulitive_nodes[i]))/75 for i in range(len(cummulitive_nodes))]
    return percentage_of_nodes_covered, range(1, len(ssds) + 1)


lams = plot_variation_in_ssd_lam()
ams = plot_variation_in_ssd_am()
plt.subplot(211)
plt.plot(ams[1], ams[0])
plt.plot(lams[1], lams[0])
plt.xlabel('UC Rank')
plt.ylabel('SSD')

n_am = plot_percentage_nodes_ssd_am()
n_lam = plot_percentage_nodes_ssd_lam()
plt.subplot(212)
plt.plot(n_am[1], n_am[0])
plt.plot(n_lam[1], n_lam[0])
plt.xlabel('UC Rank')
plt.ylabel('%Nodes')


plt.show()
