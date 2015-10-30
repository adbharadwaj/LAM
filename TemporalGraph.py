__author__ = 'adb'

import math
import networkx as nx
from LevelwiseApriori import LevelwiseApriori
from LevelwiseAprioriLAM import LevelwiseAprioriLAM

class TemporalGraph:
    """
    A Temporal Graph is list of Directed Graphs
    """
    def __init__(self, T):
        self.T = T

    def __init__(self):
        # empty graph at 0 timestamp
        self.T = [nx.Graph()]

    def __len__(self):
        """
        Returns number of static graphs in the temporal graph
        :return: int
        """
        # subtracting 1 to exclude the case of timestamp 0
        return len(self.T) - 1

    def __str__(self):
        """
        Returns string representation of temporal graph
        :return: str
        """
        return 'Size: ' + str(len(self)) + ', Order: ' + str(self.order())

    def getEnsemble(self):
        """
        Returns the ensemble of digraphs
        :return: list of digraph object
        """
        return self.T

    def nodes(self):
        """
        Returns the nodes in the temporal graph
        :return: list of nodes
        """
        nodes = []
        for G in self.T:
            nodes = list(set(G.nodes()) | set(nodes))
        return nodes

    def order(self):
        """
        Returns number of nodes in the temporal graph
        :return: int
        """
        return len(self.nodes())

    def add_node(self, v, **attr):
        """
        Add a single node v and updates node attributes
        :param v: node
        :return: None
        """
        for G in self.T:
            G.add_node(v, attr)

    def add_edge(self, timestamp, v1, v2, **attr):
        """
        Add a single edge from v1 to v2 and updates edge attributes
        :param t: int - timestamp at which the edge exists
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: None
        """
        if timestamp > len(self.T) - 1:
            self.add_graph(timestamp)
        self.T[timestamp].add_edge(v1, v2, attr)

    def add_graph(self, timestamp):
        """
        Add a digraph at given timestamp
        :param timestamp: int
        :return: None
        """
        G = nx.Graph(timestamp=timestamp)
        G.add_nodes_from(self.nodes())
        self.T.insert(timestamp, G)

    def has_edge(self, v1, v2):
        """
        Returns the probability that a directed edge exists from v1 to v2 in the temporal graph at any given timestamp
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: float
        """
        return float(len(self.find_edge(v1, v2))) / len(self)

    def find_edge(self, v1, v2):
        """
        Returns the list of timestamps when a directed edge exists from v1 to v2 in the temporal graph
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: list of timestamps
        """
        return [G.graph['timestamp'] for G in self.T if G.has_edge(v1, v2) > 0]

    def find_subgraph(self, G):
        """
        Returns the list of timestamps when the subgraph G is present in temporal graph
        :param G: digraph
        :return: list of timestamps
        """
        if G.size() > 0:
            timestamps = self.find_edge(G.edges()[0][0], G.edges()[0][1])
        else:
            return []

        for v1, v2 in G.edges():
            timestamps = list(set(timestamps).intersection(set(self.find_edge(v1, v2))))
        return timestamps

    def find_edges(self, edgeList):
        """
        Returns the list of timestamps when the given edgelist is present in temporal graph
        :param G: edgeList
        :return: list of timestamps
        """
        edge_timestamps = []
        for v1, v2 in edgeList:
            timestamps = []
            for G in self.T:
                if G.has_edge(v1, v2):
                    timestamps.append(G.graph['timestamp'])
            if len(timestamps) > 0:
                edge_timestamps.append(timestamps)

        if len(edge_timestamps) < 0:
            results = []
        else:
            results = edge_timestamps[0]
        for timestamps in edge_timestamps:
            results = list(set(results).intersection(set(timestamps)))
        # print(edgeList, results)
        return results

    def has_edges(self, edgeList):
        """
        Returns the probability that the given edgelist is present in temporal graph
        :param G: edgeList
        :return: float
        """
        return float(len(self.find_edges(edgeList))) / len(self)

    def has_subgraph(self, G):
        """
        Returns the probability that the subgraph G is present in temporal graph
        :param G: digraph
        :return: float
        """
        return float(len(self.find_subgraph(G))) / len(self)

    def subgraph_divergence(self, U):
        """
        Returns the subgraph divergence for the given set of nodes U
        :param U: list of nodes
        :return: float
        """
        sd = TemporalGraph.__nCr(len(U), 2)
        subgraphOccurences = TemporalGraph.__remove_duplicates([self.find_edges(G.edges()) for G in self.subgraph(U) if G.size() > 0])
        subgraphOccurences = TemporalGraph.prune(subgraphOccurences)
        probs = [float(len(o))/len(self) for o in subgraphOccurences]
        probs.append(1-sum(probs))
        for p in probs:
            if p > 0:
                sd += p * math.log2(p)
        return sd

    def scaled_subgraph_divergence(self, U):
        """
        Returns the subgraph divergence for the given set of nodes U
        :param U: list of nodes
        :return: float (value <= 1)
        """
        return self.subgraph_divergence(U)/TemporalGraph.__nCr(len(U), 2)


    def subgraph(self, nodes):
        """
        Returns the temporal graph induced on given nodes
        :param nodes: list of nodes
        :return: temporal graph
        """
        return [G.subgraph(nodes) for G in self.T]

    def maximal_phi_sd_ucs(self, phi):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.subgraph_divergence(x) <= phi, self.nodes())

    def phi_sd_ucs(self, phi):
        return LevelwiseApriori.freq_itemsets((lambda x: self.subgraph_divergence(x) <= phi), self.nodes())

    def maximal_sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes())

    def sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes())

    def maximal_lam_ssd_ucs(self, sigma):
        return LevelwiseAprioriLAM.maximal_freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes())

    @staticmethod
    def __nCr(n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)

    @staticmethod
    def __remove_duplicates(l):
        """
        Removes the duplicates from the given list
        :param l: list
        :return: list
        """
        s = set(tuple(x) for x in l)
        return sorted([list(x) for x in s], key=len)