'''
Input - A graph G and parameter phi s.t phi >= 0

Output - All phi-SD-UCs
'''

import itertools
import networkx as nx
import random
import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

'''
Enumerates all phi-SD-UCs for Temporal graph G and parameter phi s.t phi >= 0
'''
def sdminer(G, phi):
    output = []
    # S is the current candidate set
    S = generate_initial_candidates(G)
    while(len(S)>0):
        T = []
        for U in S:
            if (subgraph_divergence(G, U) <= phi):
                output.append(U)
                T.append(U)
        S = generate_candidates(G, T)
    print(output)

'''
Returns the subgraph divergence value for the given set of nodes U in the given temporal graph G
Output: float
Input:
G - Temporal Graph
U - list of nodes
'''
def subgraph_divergence(G, U):
    nCr(len(U), 2)
    return random.uniform(0.0, 1.0)


'''
Returns set of candidates with k + 1 nodes using set of candidates with k nodes
Output: List of lists of size k+1
Input:
G - Temporal Graph
T - list of lists of size k
'''
def generate_candidates(G, T):
    candidates = set()
    for a in T:
        for b in T:
            union = set(a).union(set(b))
            # here k = len(set(a))
            if len(union) == len(set(a)) + 1 and set(a) != set(b):
                candidates.add(tuple(union))
    # returning set of candidates with k + 1 nodes
    return list(candidates)


'''
Returns a list of subsets of size m in S
Input:
S - Given set
m - Size of the subsets returned
'''
def find_subsets(S,m):
    return list(set(itertools.combinations(S, m)))

'''
Returns the list of initial candidates of UCs
Input:
G - Given graph
'''
def generate_initial_candidates(G):
    # We start with subsets of size 2
    return find_subsets(G.nodes(), 2)

G = nx.complete_graph(5)
phi = 0.5
# sdminer(G, phi)
