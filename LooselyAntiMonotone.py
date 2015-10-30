from LevelwiseApriori import LevelwiseApriori

__author__ = 'adb'


class LooselyAntiMonotone:
    @staticmethod
    def generate_candidates(k_freq_itemsets, constraint, items):
        """
        Returns set of candidates with k + 1 nodes using set of candidates with k nodes and also returns support data which contains the parent child relationship.
        :param k_freq_itemsets: List of frequent itemsets of size k
        :param constraint: function which returns boolean value
        :param items: list of singleton items in the dataset
        :return: List of candidates of size k+1, dictionary of support data with child -> parent mapping
        """
        candidates = set()
        support_data = {}
        for a in items:
            for b in k_freq_itemsets:
                k = len(b)
                union = tuple(sorted(set(b).union({a})))
                if len(union) == k + 1 and constraint(list(union)):
                    if union not in candidates:
                        candidates.add(union)
                        if union not in support_data:
                            support_data[tuple(union)] = [b]
                        else:
                            support_data[tuple(union)].extend([b])
        # returning set of candidates with k + 1 nodes
        return list(candidates), support_data


