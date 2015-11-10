from pprint import pprint
import sys
import collections
import itertools
from Ensemble import Ensemble
from EquivalenceClass import EquivalenceClass
import matplotlib.pyplot as plt

__author__ = 'adb'


def compute_all_possible_labelled_graphs(nodes):
    nodes = sorted(nodes)
    all_possible_edges = list(itertools.combinations(nodes, 2))
    num_of_possible_edges = len(all_possible_edges)
    all_possible_graphs = collections.OrderedDict()
    for edges in range(0, num_of_possible_edges + 1):
        for edgelist in list(itertools.combinations(all_possible_edges, edges)):
            all_possible_graphs[str(list(edgelist))] = []

    return all_possible_graphs


def compute_subgraph_distribution_for_nodes(ensemble, nodes):
    found_subgraphs = ensemble.find_subgraphs_induced_by_nodes(nodes)
    ordered_subgraphs = compute_all_possible_labelled_graphs(nodes)
    for edgelist in found_subgraphs.keys():
        ordered_subgraphs[edgelist] = found_subgraphs[edgelist]
    return ordered_subgraphs

def compute_subgraph_freq_distribution_for_nodes(ensemble, nodes):
    d = compute_subgraph_distribution_for_nodes(ensemble, nodes)
    return tuple([len(v) for k, v in d.items()])


def test_equivalence_partition(iterable_list, relation = lambda x, y: x == y):
    classes, partitions, ids = EquivalenceClass.equivalence_enumeration(
        iterable_list,
        relation
    )
    EquivalenceClass.check_equivalence_partition(classes, partitions, relation)
    # for c in classes: print(c)
    # for o, c in partitions.items(): print(o, ':', c)
    return classes, partitions

with open('sephone', 'r') as f:
    T = Ensemble()
    for line in f:
        line = line.strip()
        timestamp, v1, v2 = line.split('\t', 2)
        if v1 != v2:
            T.add_edge(timestamp, int(v1), int(v2))
        else:
            T.add_node(int(v1))

nodes_freq_dist_map = collections.OrderedDict()
ssd_buckets = collections.OrderedDict()
with open('hyperedge-results/sephone/lam/top-1024-hyperedges.tsv', 'r') as f:
    for line in f:
        line = line.strip()
        nodes = [int(n) for n in line.split('\t')[:-1]]
        ssd = float(line.split('\t')[-1])
        if ssd in ssd_buckets:
            ssd_buckets[ssd].append(nodes)
        else:
            ssd_buckets[ssd] = [nodes]
        dist = compute_subgraph_freq_distribution_for_nodes(T, nodes)
        if str(dist) in nodes_freq_dist_map:
            nodes_freq_dist_map[str(dist)].append(nodes)
        else:
            nodes_freq_dist_map[str(dist)] = [nodes]

# pprint(ssd_buckets)
# pprint(len(nodes_freq_dist_map.keys()))
for k,v in nodes_freq_dist_map.items():
    print(str(k) + '\t' + str(v))
# for tup in tups:
#     print(tup)
# classes, partitions = test_equivalence_partition(iter(tups))
# print(len(classes), len(tups))
# for c in classes:
#     print(c)
# pprint(compute_subgraph_distribution_for_nodes(T, [12, 36, 44, 68]))
# d = compute_subgraph_distribution_for_nodes(T, [5, 11, 63])
# pprint(tuple([len(v) for k, v in d.items()]))
# pprint(T.find_subgraphs_induced_by_nodes([4, 31, 56, 58]))
# pprint(compute_subgraph_distribution_for_nodes(T, [4, 31, 56, 58]))