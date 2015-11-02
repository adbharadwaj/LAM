__author__ = 'adb'

import math
import itertools
import networkx as nx
from TemporalGraph import TemporalGraph



class SDMiner:
    """
    A levelwise computing all maximal phi-SD-UCs
    """
    @staticmethod
    def enumerate_phi_sd_ucs(temporalGraph,  phi):
        """
        Returns list of phi-SD-UCs in the temporal graph for given parameter phi
        :param temporalGraph: TemporalGraph object
        :param phi: float (phi >= 0)
        :return: list of list of nodes
        """

        output = []
        # S is the current candidate set
        S = SDMiner.__generate_initial_candidate(temporalGraph)
        while len(S) > 0:
            T = []
            for U in S:
                if temporalGraph.compute_subgraph_divergence(U) <= phi:
                    output.append(U)
                    T.append(U)
            S, support_data = SDMiner.__generate_candidates(T)
        return output

    @staticmethod
    def enumerate_maximal_phi_sd_ucs(temporalGraph,  phi):
        """
        Returns list of maximal phi-SD-UCs in the temporal graph for given parameter phi
        :param temporalGraph: TemporalGraph object
        :param phi: float (phi >= 0)
        :return: list of list of nodes
        """

        support_data = {}
        # deletes is used to mark the deletes
        deletes = []

        # S is the current candidate set
        S = SDMiner.__generate_initial_candidate(temporalGraph)
        while len(S) > 0:
            T = []
            for U in S:
                if temporalGraph.compute_subgraph_divergence(U) <= phi:
                    deletes.extend([parent for parent in support_data if U in support_data])
                    T.append(U)
            S, support_data = SDMiner.__generate_candidates(T)


        return [x for x in T if x not in deletes]

    @staticmethod
    def __generate_candidates(T):
        """
        Returns set of candidates with k + 1 nodes using set of candidates with k nodes and also returns support data which contains the parent child relationship.
        :param T: List of candidates of size k
        :return: List of candidates of size k+1, dictionary of support data
        """
        candidates = set()
        support_data = dict()
        for a in T:
            for b in T:
                union = tuple(set(a).union(set(b)))
                # here k = len(set(a))
                if len(union) == len(set(a)) + 1 and set(a) != set(b):
                    candidates.add(union)
                    if union in support_data:
                        support_data[tuple(union)].append([a, b])
                    else:
                        support_data[tuple(union)] = list([a, b])

        # returning set of candidates with k + 1 nodes
        return list(candidates), support_data

    @staticmethod
    def __generate_initial_candidate(T):
        """
        Returns the list of initial candidates of UCs of size 2
        :param T: temporal graph
        :return: list of list of nodes
        """
        return SDMiner.__find_subsets(T.nodes(), 2)

    @staticmethod
    def __find_subsets(S, m):
        """
        Returns a list of subsets of size m in itemlist S
        :param S: list of items
        :param m: size of the subsets returned
        :return: list of list of items
        """
        return list(set(itertools.combinations(S, m)))