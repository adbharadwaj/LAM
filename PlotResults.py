import matplotlib.pyplot as plt
import sys
import numpy as np
from Ensemble import Ensemble

__author__ = 'adb'


datafile = 'sephone'
results_folder = 'hyperedge-results/' + datafile
graph_summary_file = 'hyperedge-results/' + datafile + '/' + datafile + '.summary'
lam_results_folder = results_folder + '/lam'
am_results_folder = results_folder + '/am'


def compute_percentage_of_nodes_covered(nodes, num_of_nodes):
    cummulitive_nodes = []
    for i in range(len(nodes)):
        if i == 0:
            cummulitive_nodes.insert(i, nodes[i])
        else:
            cummulitive_nodes.insert(i, list(set(cummulitive_nodes[i-1]).union(set(nodes[i]))))
    return [float(100*len(cummulitive_nodes[i]))/num_of_nodes for i in range(len(cummulitive_nodes))]

def compute_ssd_of_remaining_nodes(nodes_in_ucs, ensemble):
    rem_nodes = set(ensemble.nodes()).difference(set(nodes_in_ucs))
    return ensemble.compute_scaled_subgraph_divergence(list(rem_nodes))

def plot_ssd_vs_rank(max_rank):
    with open(am_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        am_ssds = [line.split('\t')[-1] for line in f]
    with open(lam_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        lam_ssds = [line.split('\t')[-1] for line in f]

    plt.subplot(211)
    plt.plot([i for i in range(1, len(am_ssds)+1)], am_ssds, label='am')
    plt.plot([i for i in range(1, len(lam_ssds)+1)], lam_ssds, label='lam')
    plt.legend(loc='lower right')
    plt.xlabel('UC Rank')
    plt.ylabel('SSD')


def plot_percent_of_nodes_vs_rank(max_rank, num_of_nodes):
    with open(am_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        am_nodes = [line.split('\t')[:-1] for line in f]
        am_percentage_of_nodes_covered = compute_percentage_of_nodes_covered(am_nodes, num_of_nodes)

    with open(lam_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        lam_nodes = [line.split('\t')[:-1] for line in f]
        lam_percentage_of_nodes_covered = compute_percentage_of_nodes_covered(lam_nodes, num_of_nodes)

    plt.subplot(212)
    plt.plot([i for i in range(1, len(am_percentage_of_nodes_covered)+1)], am_percentage_of_nodes_covered, label='am')
    plt.plot([i for i in range(1, len(lam_percentage_of_nodes_covered)+1)], lam_percentage_of_nodes_covered, label='lam')
    plt.legend(loc='lower right')
    plt.xlabel('UC Rank')
    plt.ylabel('% Nodes')

def plot_ssd_of_uncovered_nodes_vs_rank(max_rank, T):
    with open(am_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        am_ssds = [line.split('\t')[-1] for line in f]
    with open(am_results_folder + '/top-' + str(max_rank) + '-hyperedges.tsv', 'r') as f:
        am_rem_ssds = [compute_ssd_of_remaining_nodes(line.split('\t')[:-1], T) for line in f]
    print(am_rem_ssds)
    plt.plot([i for i in range(1, len(am_ssds)+1)], am_ssds, label='UCs')
    plt.plot([i for i in range(1, len(am_rem_ssds)+1)], am_rem_ssds, label='Remaining Nodes')
    plt.legend(loc='lower right')
    plt.xlabel('UC Rank')
    plt.ylabel('SSD')

def plot_ucs_size_composition_vs_ssd_cutoff(threeUC, fourUC, fiveUC, ssd_range):
    N = len(ssd_range)

    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, threeUC, width, color='r')
    p2 = plt.bar(ind, fourUC, width, color='y', bottom=threeUC)
    p3 = plt.bar(ind, fiveUC, width, color='g', bottom=[i+j for i,j in zip(threeUC, fourUC)])

    plt.ylabel('#UCs')
    plt.xlabel('SSD Cutoffs')
    plt.title('Hyperedge Composition')
    plt.xticks(ind + width/2., tuple(ssd_range))
    # plt.yticks(np.arange(0, threeUC[-1], 5))
    plt.legend((p1[0], p2[0], p3[0]), ('UCs of size 3', 'UCs of size 4', 'UCs of size 5'), loc='upper left')

def plot_num_of_k_size_ucs_vs_ssd_cutoff_for_am(ssd_range):
    size_map_for_ssd_range = {}
    for ssd in ssd_range:
        size_map_for_ssd_range[ssd] = {3: 0, 4: 0, 5: 0, 6: 0}
    for ssd_cutoff in ssd_range:
        with open(am_results_folder + '/hyperedges-sigma-' + str(ssd_cutoff) + '.tsv', 'r') as f:
            for line in f:
                 size_map_for_ssd_range[ssd_cutoff][len(line.split('\t')[:-1])] +=1
    threeS = []
    fourS = []
    fiveS = []
    for ssd_cutoff in ssd_range:
        threeS.append(size_map_for_ssd_range[ssd_cutoff][3])
        fourS.append(size_map_for_ssd_range[ssd_cutoff][4])
        fiveS.append(size_map_for_ssd_range[ssd_cutoff][5])

    plot_ucs_size_composition_vs_ssd_cutoff(threeS, fourS, fiveS, ssd_range)

    return size_map_for_ssd_range



def plot_num_of_k_size_ucs_vs_ssd_cutoff_for_lam(ssd_range):
    size_map_for_ssd_range = {}
    for ssd in ssd_range:
        size_map_for_ssd_range[ssd] = {3: 0, 4: 0, 5: 0, 6: 0}
    for ssd_cutoff in ssd_range:
        with open(lam_results_folder + '/hyperedges-sigma-' + str(ssd_cutoff) + '.tsv', 'r') as f:
            for line in f:
                 size_map_for_ssd_range[ssd_cutoff][len(line.split('\t')[:-1])] +=1
    threeS = []
    fourS = []
    fiveS = []
    for ssd_cutoff in ssd_range:
        threeS.append(size_map_for_ssd_range[ssd_cutoff][3])
        fourS.append(size_map_for_ssd_range[ssd_cutoff][4])
        fiveS.append(size_map_for_ssd_range[ssd_cutoff][5])

    plot_ucs_size_composition_vs_ssd_cutoff(threeS, fourS, fiveS, ssd_range)

    return size_map_for_ssd_range


with open(graph_summary_file, 'r') as f:
    for line in f:
        line = line.strip()
        summary = line.split('\t', 4)
        num_of_timestamps, num_of_nodes, min_num_of_edges, max_num_of_edges, total_num_of_edges = int(summary[0]), int(summary[1]), int(summary[2]), int(summary[3]), int(summary[4])

with open(datafile, 'r') as f:
    T = Ensemble()
    for line in f:
        line = line.strip()
        timestamp, v1, v2 = line.split('\t', 2)
        if v1 != v2:
            T.add_edge(timestamp, int(v1), int(v2))
        else:
            T.add_node(int(v1))

# plot_ssd_vs_rank(1024)
# plot_percent_of_nodes_vs_rank(1024, num_of_nodes)
# plot_ssd_of_uncovered_nodes_vs_rank(2048, T)
# print(plot_num_of_k_size_ucs_vs_ssd_cutoff_for_am([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]))
print(plot_num_of_k_size_ucs_vs_ssd_cutoff_for_lam([0.1, 0.2, 0.3, 0.4,  0.5, 0.6]))

plt.show()