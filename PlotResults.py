import matplotlib.pyplot as plt
import sys
from Ensemble import Ensemble

__author__ = 'adb'


datafile = 'datahospital'
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




with open(graph_summary_file, 'r') as f:
    for line in f:
        line = line.strip()
        summary = line.split('\t', 4)
        num_of_timestamps, num_of_nodes, min_num_of_edges, max_num_of_edges, total_num_of_edges = int(summary[0]), int(summary[1]), int(summary[2]), int(summary[3]), int(summary[4])


plot_ssd_vs_rank(128)
plot_percent_of_nodes_vs_rank(128, num_of_nodes)
plt.show()