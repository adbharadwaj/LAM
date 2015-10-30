__author__ = 'adb'

import itertools

class LevelwiseApriori:
    """
    Implements the levelwise Apriori Algorithm
    """

    @staticmethod
    def freq_itemsets(constraint, items, generate_candidates):
        """
        Returns list of all frequent itemsets which satisfy the given constraint
        :param constraint: function which return boolean value
        :param items: list of singleton items
        :return: list of itemsets
        """
        output, deletes = LevelwiseApriori.__compute_freq_itemsets(constraint, items, generate_candidates)
        return output

    @staticmethod
    def __compute_freq_itemsets(constraint, items, generate_candidates):
        """
        Returns list of all frequent itemsets which satisfy the given constraint and also returns the itemsets which do not satisfy the maximality constraint
        :param constraint: function which return boolean value
        :param items: list of singleton items
        :return: list of itemsets
        """
        support_data = {}
        output = set()
        # deletes is used to mark the deletes
        deletes = set()

        # S is the current candidate set
        S = LevelwiseApriori.__generate_initial_candidate(items, constraint)
        # print('Size of S = %d, Size of output = %d' % (len(S), len(output)))
        while len(S) > 0:
            T = set()
            for U in S:
                U = tuple(sorted(list(U)))
                output.add(U)
                T.add(U)
                if U in support_data:
                    for parent in support_data[U]:
                        deletes.add(parent)
            S, support_data = generate_candidates(T, constraint, items)
            # print('Size of T = %d, Size of S = %d, Size of output = %d, Size of deletes = %d' % (len(T), len(S), len(output), len(deletes)))
        return output, deletes

    @staticmethod
    def maximal_freq_itemsets(constraint, items, generate_candidates):
        """
        Returns list of maximal frequent itemsets which satisfy the given constraint
        :param constraint: function which return boolean value
        :param items: list of singleton items
        :return: list of itemsets
        """
        output, deletes = LevelwiseApriori.__compute_freq_itemsets(constraint, items, generate_candidates)
        return [x for x in output if x not in deletes]

    @staticmethod
    def __generate_initial_candidate(items, constraint):
        """
        Returns the list of initial candidates of UCs of size 2
        :param items: list of singleton items
        :return: list of list of nodes
        """
        return [tuple(sorted(list(U))) for U in LevelwiseApriori.find_subsets(items, 2) if constraint(list(U))]

    @staticmethod
    def find_subsets(S, m):
        """
        Returns a list of subsets of size m in itemlist S
        :param S: list of items
        :param m: size of the subsets returned
        :return: list of list of items
        """
        return list((itertools.combinations(S, m)))