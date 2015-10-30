__author__ = 'adb'

import math
import networkx as nx
from LevelwiseApriori import LevelwiseApriori
from AntiMonotone import AntiMonotone
from LooselyAntiMonotone import LooselyAntiMonotone

class Ensemble:
    """
    An ensemble is list of Undirected Graphs
    """
    def __init__(self, T):
        self.T = T

    def __init__(self):
        # empty graph at 0 timestamp
        self.T = [nx.Graph(timestamp=0)]

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
        return 'Timestamps: ' + str(len(self)) + ', Order: ' + str(self.order()) + ', Size: ' + str(self.size())

    def getEnsemble(self):
        """
        Returns the list of networkx graph objects
        :return: list of networkx graph object
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

    def size(self):
        return sum([G.size() for G in self.T])

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
        Add a graph at given timestamp
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

        timestamps = [g.graph['timestamp'] for g in self.T if g.size() > 0 and Ensemble.matches(G, g.subgraph(G.nodes()))]
        # print(timestamps)
        return timestamps

    def find_subgraphs_induced_by_nodes(self, nodes):
        found_subgraphs = {}
        for G in self.T:
            if G.size() > 0:
                subgraph = str(sorted([tuple(sorted(e)) for e in G.subgraph(nodes).edges()],  key=lambda tup: tup[0]))
                if subgraph in found_subgraphs:
                    found_subgraphs[subgraph].append(G.graph['timestamp'])
                else:
                    found_subgraphs[subgraph] = [G.graph['timestamp']]
        return found_subgraphs

    @staticmethod
    def matches(G1, G2):
        """
        Returns true if G1 matches with G2

        G1 matches with G2 if their edgelist is exactly same
        :return: boolean
        """
        edges_g1 = set(G1.edges())
        edges_g2 = set(G2.edges())
        edges = edges_g1.symmetric_difference(edges_g2)
        return len(edges) == 0 and len(edges_g1) == len(edges_g2)

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
        # We initialize the subgraph divergence with number of combinations for set U
        subgraph_divergence = Ensemble.compute_combinations(len(U), 2)
        # this list doesnt include the timestamps of subgraphs with no edges i.e size 0
        induced_subgraphs_dict = self.find_subgraphs_induced_by_nodes(U)
        probability_of_subgraphs = [float(len(timestamps))/len(self) for timestamps in induced_subgraphs_dict.values()]
        for p in probability_of_subgraphs:
            if p > 0.0:
                subgraph_divergence += p * math.log2(p)
        return subgraph_divergence

    def scaled_subgraph_divergence(self, U):
        """
        Returns the subgraph divergence for the given set of nodes U
        :param U: list of nodes
        :return: float (value <= 1)
        """
        ssd = self.subgraph_divergence(U)/Ensemble.compute_combinations(len(U), 2)
        return ssd

    def subgraph(self, nodes):
        """
        Returns the temporal graph induced on given nodes
        :param nodes: list of nodes
        :return: temporal graph
        """
        return [G.subgraph(nodes) for G in self.T]

    def maximal_phi_sd_ucs(self, phi):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.subgraph_divergence(x) <= phi, self.nodes(), AntiMonotone.generate_candidates)

    def phi_sd_ucs(self, phi):
        return LevelwiseApriori.freq_itemsets((lambda x: self.subgraph_divergence(x) <= phi), self.nodes(), AntiMonotone.generate_candidates)

    def maximal_sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes(), AntiMonotone.generate_candidates)

    def sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes(), AntiMonotone.generate_candidates)

    def maximal_lam_sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.scaled_subgraph_divergence(x) <= sigma, self.nodes(), LooselyAntiMonotone.generate_candidates)

    def generate_antimonotone_hyperedges_report(self, sigma):
        '''
        Prints the report in following format
        Size of Hyperedge   Tab seperated list of nodes in the hyperedge    ssd of the hyperdge

        Note: We are gonna ignore hyperdges of size 2 for report purposes as they are not useful for our analysis
        :param sigma:
        :return: None
        '''

        hyperedges = sorted(self.maximal_sigma_ssd_ucs(sigma), key=len)
        for hyperedge in hyperedges:
            if len(hyperedge) != 2:
                print('%s\t%s\t%s' % (len(hyperedge), list_to_tab_seperated_string(hyperedge), self.scaled_subgraph_divergence(list(hyperedge))))
        return None

    def generate_looselyantimonotone_hyperedges_report(self, sigma):
        '''
        Prints the report in following format
        Size of Hyperedge   Tab seperated list of nodes in the hyperedge    ssd of the hyperdge

        Note: We are gonna ignore hyperdges of size 2 for report purposes as they are not useful for our analysis
        :param sigma:
        :return: None
        '''

        hyperedges = sorted(self.maximal_lam_sigma_ssd_ucs(sigma), key=len)
        for hyperedge in hyperedges:
            if len(hyperedge) != 2:
                print('%s\t%s\t%s' % (len(hyperedge), list_to_tab_seperated_string(hyperedge), self.scaled_subgraph_divergence(list(hyperedge))))


    @staticmethod
    def compute_combinations(n,r):
        f = math.factorial
        return f(n) / f(r) / f(n-r)


def list_to_tab_seperated_string(l):
        result = ''
        for i in l:
            result += ('%s\t' % i)
        return result.rstrip()
