import math
import networkx as nx
from LevelwiseApriori import LevelwiseApriori
from AntiMonotone import AntiMonotone
from LooselyAntiMonotone import LooselyAntiMonotone

__author__ = 'adb'


class Ensemble:
    """
    An ensemble is dictionary of Undirected Graph where key is timestamp and
    value is networkx object of the static graph at that timestamp
    """

    def __init__(self, ensemble=None):
        # empty graph at 0 timestamp
        if ensemble:
            self.time_graph_dict = ensemble
        else:
            self.time_graph_dict = dict()

    def __len__(self):
        """
        Returns number of static graphs in the ensemble
        :return: int
        """
        return len(self.time_graph_dict)

    def __str__(self):
        """
        Returns string representation of ensemble
        :return: str
        """
        return '#Timestamps: ' + str(len(self)) + ', #Nodes: ' + str(self.order()) + ', #Edges: ' + str(self.size())

    def get_num_of_timestamps(self):
        """
        Returns the number of timestamps in the ensemble
        :return: int
        """
        return len(self)

    def get_static_graph_at_timestamp(self, t):
        """
        Returns the reference to networkx object at timestamp t
        :return: networkx object
        """
        if t in self.get_all_timestamps():
            return self.time_graph_dict[t]
        else:
            return None

    def get_all_timestamps(self):
        """
        Returns the list of timestamps in the ensemble
        :return: list
        """
        return self.time_graph_dict.keys()

    def get_all_static_graphs(self):
        """
        Returns the list of networkx graph objects
        :return: list of networkx graph object
        """
        return self.time_graph_dict.values()

    def nodes(self):
        """
        Returns the nodes in the ensemble
        :return: list of nodes
        """
        nodes = []
        for G in self.get_all_static_graphs():
            nodes = list(set(G.nodes()) | set(nodes))
        return nodes

    def size(self):
        """
        Returns the number of edges in the ensemble

        Note: each edge at timestamp is a unique edge

        :return: int
        """
        return sum([G.size() for G in self.get_all_static_graphs()])

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
        for G in self.get_all_static_graphs():
            G.add_node(v, attr)

    def add_edge(self, t, v1, v2, **attr):
        """
        Add a single edge from v1 to v2 and updates edge attributes
        :param t: int - timestamp at which the edge exists
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: None
        """
        if t not in self.get_all_timestamps():
            self.add_graph(t)
        self.get_static_graph_at_timestamp(t).add_edge(v1, v2, attr)

    def add_graph(self, timestamp):
        """
        Add a graph at given timestamp
        :param timestamp: int
        :return: None
        """
        if timestamp not in self.get_all_timestamps():
            graph = nx.Graph(timestamp=timestamp)
            graph.add_nodes_from(self.nodes())
            self.time_graph_dict[timestamp] = graph

    def has_edge(self, v1, v2):
        """
        Returns the probability that an edge exists from v1 to v2 in the ensemble at given timestamp
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: float
        """
        return float(len(self.find_edge(v1, v2))) / self.get_num_of_timestamps()

    def find_edge(self, v1, v2):
        """
        Returns the list of timestamps when an edge exists from v1 to v2 in the ensemble
        :param v1: node 1 (int or str)
        :param v2: node 2 (int or str)
        :return: list of timestamps
        """
        return [G.graph['timestamp'] for G in self.get_all_static_graphs() if G.has_edge(v1, v2)]

    def find_subgraph(self, graph):
        """
        Returns the list of timestamps when the subgraph 'graph' is present in the ensemble
        :param graph: graph object
        :return: list of timestamps
        """

        timestamps = [g.graph['timestamp'] for g in self.get_all_static_graphs() if
                      Ensemble.is_matching_graph(graph, g.subgraph(graph.nodes()))]
        return timestamps

    def find_subgraphs_induced_by_nodes(self, nodes):
        """
        Returns a dictionary of edgelists mapped to timestamp at which the given edgelist is induced by the given nodes
        :param nodes: list of nodes
        :return: dict {string representation of edgelist: list of timestamps}
        """
        found_subgraphs = {}
        for G in self.get_all_static_graphs():
            if G.size() > 0:
                subgraph = str(sorted([tuple(sorted(e)) for e in G.subgraph(nodes).edges()], key=lambda tup: (tup[0], tup[1])))
                if subgraph in found_subgraphs:
                    found_subgraphs[subgraph].append(G.graph['timestamp'])
                else:
                    found_subgraphs[subgraph] = [G.graph['timestamp']]
        return found_subgraphs

    @staticmethod
    def is_matching_graph(g1, g2):
        """
        Returns true if g1 matches with g2

        g1 matches with g2 if their edgelist is exactly same
        :return: boolean
        """
        edges_g1 = set(g1.edges())
        edges_g2 = set(g2.edges())
        edges = edges_g1.symmetric_difference(edges_g2)
        return len(edges) == 0 and len(edges_g1) == len(edges_g2)

    def has_subgraph(self, graph):
        """
        Returns the probability that the subgraph graph is present in temporal graph
        :param graph: digraph
        :return: float
        """
        return float(len(self.find_subgraph(graph))) / len(self)

    def compute_subgraph_divergence(self, nodes):
        """
        Returns the subgraph divergence for the given set of nodes nodes
        :param nodes: list of nodes
        :return: float
        """
        # We initialize the subgraph divergence with number of combinations for set nodes of size 2
        subgraph_divergence = Ensemble.compute_combinations(len(nodes), 2)
        induced_subgraphs_dict = self.find_subgraphs_induced_by_nodes(nodes)
        probability_of_subgraphs = [float(len(timestamps)) / self.get_num_of_timestamps() for timestamps in
                                    induced_subgraphs_dict.values()]
        for p in probability_of_subgraphs:
            if p > 0.0:
                subgraph_divergence += p * math.log2(p)
        return subgraph_divergence

    def compute_scaled_subgraph_divergence(self, nodes):
        """
        Returns the subgraph divergence for the given set of nodes nodes
        :param nodes: list of nodes
        :return: float (value <= 1)
        """
        ssd = self.compute_subgraph_divergence(nodes) / Ensemble.compute_combinations(len(nodes), 2)
        return ssd

    def maximal_phi_sd_ucs(self, phi):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.compute_subgraph_divergence(x) <= phi,
                                                      self.nodes(), AntiMonotone.generate_candidates)

    def phi_sd_ucs(self, phi):
        return LevelwiseApriori.freq_itemsets((lambda x: self.compute_subgraph_divergence(x) <= phi), self.nodes(),
                                              AntiMonotone.generate_candidates)

    def maximal_sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.compute_scaled_subgraph_divergence(x) <= sigma,
                                                      self.nodes(), AntiMonotone.generate_candidates)

    def sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.freq_itemsets(lambda x: self.compute_scaled_subgraph_divergence(x) <= sigma,
                                              self.nodes(), AntiMonotone.generate_candidates)

    def maximal_lam_sigma_ssd_ucs(self, sigma):
        return LevelwiseApriori.maximal_freq_itemsets(lambda x: self.compute_scaled_subgraph_divergence(x) <= sigma,
                                                      self.nodes(), LooselyAntiMonotone.generate_candidates)

    def generate_antimonotone_hyperedges_report(self, sigma):
        """
        Prints the report in following format
        Size of Hyperedge   Tab seperated list of nodes in the hyperedge    ssd of the hyperdge

        Note: We are gonna ignore hyperdges of size 2 for report purposes as they are not useful for our analysis
        :param sigma:
        :return: None
        """

        hyperedges = sorted(self.maximal_sigma_ssd_ucs(sigma), key=len)
        for hyperedge in hyperedges:
            if len(hyperedge) != 2:
                print('%s\t%s\t%s' % (len(hyperedge), list_to_tab_seperated_string(hyperedge),
                                      self.compute_scaled_subgraph_divergence(list(hyperedge))))
        return None

    def compute_am_sigma_hyperedges_dict(self, sigma_range):
        sigma_hyperedges_dict = {}
        for i in sigma_range:
            sigma_hyperedges_dict[i] = [sorted(hyperedge) for hyperedge in self.maximal_sigma_ssd_ucs(i) if len(hyperedge)>2]
        return sigma_hyperedges_dict

    def generate_looselyantimonotone_hyperedges_report(self, sigma):
        """
        Prints the report in following format
        Size of Hyperedge   Tab seperated list of nodes in the hyperedge    ssd of the hyperdge

        Note: We are gonna ignore hyperdges of size 2 for report purposes as they are not useful for our analysis
        :param sigma:
        :return: None
        """

        hyperedges = sorted(self.maximal_lam_sigma_ssd_ucs(sigma), key=len)
        for hyperedge in hyperedges:
            if len(hyperedge) != 2:
                print('%s\t%s\t%s' % (len(hyperedge), list_to_tab_seperated_string(hyperedge),
                                      self.compute_scaled_subgraph_divergence(list(hyperedge))))

    @staticmethod
    def compute_combinations(n, r):
        f = math.factorial
        return f(n) / f(r) / f(n - r)


def list_to_tab_seperated_string(l):
    result = ''
    for i in l:
        result += ('%s\t' % i)
    return result.rstrip()

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump
