from LevelwiseApriori import LevelwiseApriori

__author__ = 'adb'


class AntiMonotone:
    @staticmethod
    def generate_candidates(k_freq_itemsets, constraint, items):
        """
        Returns set of candidates with k + 1 nodes using set of candidates with k nodes and also returns support data which contains the parent child relationship.
        :param k_freq_itemsets: List of frequent itemsets of size k
        :param constraint: function which returns boolean value
        :param items: not used by definition of antimonotone but used by loosely antimonotone definition
        :return: List of candidates of size k+1, dictionary of support data with child -> parent mapping
        """
        candidates = set()
        support_data = {}
        for a in k_freq_itemsets:
            for b in k_freq_itemsets:
                k = len(a)
                union = tuple(sorted(set(a).union(set(b))))
                if len(union) == k + 1 and constraint(list(union)):
                    if union not in candidates:
                        parents = LevelwiseApriori.find_subsets(list(union), k)
                        if isSubSet(parents, k_freq_itemsets):
                            candidates.add(union)
                            if union not in support_data:
                                support_data[tuple(union)] = parents
        # returning set of candidates with k + 1 nodes
        return list(candidates), support_data


def isSubSet(parents, k_freq_itemsets):
    for tup in parents:
        if tuple(sorted(tup)) not in k_freq_itemsets:
            return False
    return True

