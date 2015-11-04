import sys
from Ensemble import Ensemble
import matplotlib.pyplot as plt

__author__ = 'adb'

datafile = 'rmprox'
results_folder = 'hyperedge-results/' + datafile

sigma_range = [0.01, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]


def list_to_tab_seperated_string(l):
    result = ''
    for i in l:
        result += ('%s\t' % i)
    return result.rstrip()


def update_top_k_ssd_edges(ssd_hyperedges_in_sigma_range):
    sorted_hyperedges = sorted(ssd_hyperedges_in_sigma_range, key=lambda x: x[-1])
    for i in range(16):
        write_top_k_ssd_edges(sorted_hyperedges, pow(2, i))
    return sorted_hyperedges


def write_top_k_ssd_edges(sorted_hyperedges, k):
    sorted_hyperedges = sorted_hyperedges[:k]
    with open(results_folder + '/lam/top-' + str(k) + '-hyperedges.tsv', 'w+') as f:
        for hyperedge in sorted_hyperedges:
            f.write(list_to_tab_seperated_string(list(hyperedge)) + '\n')
    print('Updated top %d hyperedges' % k)
    return None

with open(datafile, 'r') as f:
    T = Ensemble()
    for line in f:
        line = line.strip()
        timestamp, v1, v2 = line.split('\t', 2)
        if v1 != v2:
            T.add_edge(timestamp, int(v1), int(v2))
        else:
            T.add_node(int(v1))

with open(results_folder + '/' + datafile + '.summary', 'w+') as f:
    edges = [g.size() for g in T.get_all_static_graphs()]
    summary = '%d\t%d\t%d\t%d\t%d' % (T.get_num_of_timestamps(), T.order(), min(edges), max(edges), T.size())
    print('Graph Summary: %s' % summary)
    f.write(summary)

ssd_hyperedges_in_sigma_range = []
for sigma in sigma_range:
    print('Computing %s-sigma-hyperedges' % sigma)
    hyperedges = T.maximal_lam_sigma_ssd_ucs(sigma)
    ssd_hyperedges = []
    for hyperedge in hyperedges:
        if (len(hyperedge)>2):
            hyperedge = sorted(hyperedge)
            hyperedge.append(T.compute_scaled_subgraph_divergence(list(hyperedge)))
            ssd_hyperedges.append(tuple(hyperedge))
    ssd_hyperedges = sorted(ssd_hyperedges, key=lambda x: x[-1])
    print('Found %d %s-sigma-hyperedges' % (len(ssd_hyperedges), sigma))
    with open(results_folder + '/lam/hyperedges-sigma-' + str(sigma) + '.tsv', 'w+') as f:
        for hyperedge in ssd_hyperedges:
            f.write(list_to_tab_seperated_string(list(hyperedge)) + '\n')
    ssd_hyperedges_in_sigma_range.extend(ssd_hyperedges)
    ssd_hyperedges_in_sigma_range = list(set(ssd_hyperedges_in_sigma_range))
    ssd_hyperedges_in_sigma_range = update_top_k_ssd_edges(ssd_hyperedges_in_sigma_range)

print("Done")



