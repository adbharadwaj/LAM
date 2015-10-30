__author__ = 'adb'

import itertools

from LevelwiseApriori import LevelwiseApriori

class LevelwiseAprioriLAM:

    @staticmethod
    def maximal_freq_itemsets(constraint, items):
        """
        Returns list of maximal frequent itemsets which satisfy the given constraint
        :param constraint: function which return boolean value
        :param items: list of singleton items
        :return: list of itemsets
        """
        support_data = {}
        output = []
        # deletes is used to mark the deletes
        deletes = []

        # S is the current candidate set
        S = LevelwiseAprioriLAM.__generate_initial_candidate(items)
        print('Size of S = %d, Size of output = %d' % (len(S), len(output)))
        while len(S) > 0:
            T = []
            for U in S:
                if constraint(U):
                    output.append(U)
                    if U in support_data:
                        deletes.extend([parent for parent in support_data[tuple(U)]])
                    T.append(U)
            S, support_data = LevelwiseAprioriLAM.__generate_candidates(T, items)
            print('Size of T = %d, Size of S = %d, Size of output = %d, Size of deletes = %d' % (len(T), len(S), len(output), len(deletes)))
        return [x for x in output if x not in deletes]


    @staticmethod
    def __generate_candidates(T, items):
        """
        Returns set of candidates with k + 1 nodes using set of candidates with k nodes and also returns support data which contains the parent child relationship.
        :param items: list of singleton items in the dataset
        :param T: List of candidates of size k
        :return: List of candidates of size k+1, dictionary of support data
        """
        candidates = set()
        support_data = dict()
        for a in items:
            for b in T:
                if a not in b:
                    union = tuple(set(b).union({a}))
                    candidates.add(union)
                    if union in support_data:
                        support_data[tuple(union)].extend([b])
                    else:
                        support_data[tuple(union)] = list([b])

        # returning set of candidates with k + 1 nodes
        return list(candidates), support_data

    @staticmethod
    def __generate_initial_candidate(items):
        """
        Returns the list of initial candidates of UCs of size 2
        :param items: list of singleton items
        :return: list of list of nodes
        """
        return LevelwiseAprioriLAM.__find_subsets(items, 2)

    @staticmethod
    def __find_subsets(S, m):
        """
        Returns a list of subsets of size m in itemlist S
        :param S: list of items
        :param m: size of the subsets returned
        :return: list of list of items
        """
        return list(set(itertools.combinations(S, m)))