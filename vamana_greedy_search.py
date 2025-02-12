import heapq
import random
import math
import numpy as np

import networkx as nx
import matplotlib.pyplot as plt

random.seed(100)

def vamana_index(points, alpha, L, R):
    """
    Creates an in-memory index on the supplied points to efficiently
    answer approximate nearest neighbor queries.
    The N points must already be initialized as a random graph of outgoing edges with 
    maximum of log(N) outgoing edges per point.

    Args:
        points - List of N points
        alpha - Scaling factor to prune outgoing eges of a node.
        L - Maximum list of search candidates to use in graph traversal.
        R - Maximum number of outgoing edges of a node. Must be less than log(N) for good results.
    """
    s = mediod(points)
    size = len(points)

    # Create array of randomly shuffled indices of points
    # for random insertion into graph.
    sigma = [i for i in range(len(points))]
    random.shuffle(sigma)

    offset = len(points) // 4

    for i in range(size):
        sigma_idx = sigma[i]
        current_point = points[sigma_idx]
        _, visited = greedy_search(s, points[sigma_idx], 1, L)
        robust_prune(current_point, visited, alpha, R)

        for other in neighbors(current_point):
            outgoing = neighbors(other)
            outgoing.add(current_point)

            if len(outgoing) > R:
                robust_prune(other, outgoing, alpha, R)
            else:
                set_neighbors(other, outgoing)            
        
        if i % offset == 0:
            plot_graph(points, f'experiments/iterations/iteration_{alpha}_{i}.png')

    plot_graph(points, f'experiments/iterations/iteration_{alpha}_{i}.png')

def greedy_search(source_node, query_node, k, L):
    """
    Find the k nearest neighbors to query_node starting traversal from source_node.
    Limit the maximum search candidates at any point to L.

    Returns:
        The k approximate nearest neighbors and the set of nodes visited to find the nearest neighbors.
    """
    candidates = set([source_node])
    visited = set()
    distance_to_query_node_fn = lambda p: distance(p, query_node)
    while candidates - visited:
        p_star = min(candidates - visited, key=distance_to_query_node_fn)
        candidates = candidates.union(neighbors(p_star))
        visited.add(p_star)

        if len(candidates) > L:
            candidates = set(heapq.nsmallest(L, candidates, key=distance_to_query_node_fn))

    closest_k_points = heapq.nsmallest(k, candidates, key=distance_to_query_node_fn)
    return [closest_k_points, visited]

def robust_prune(source_node, candidates, alpha, R):
    """
    Prunes the list of candidates and sets the outgoing edges of the supplied node.
    """
    candidates = set(candidates).union(neighbors(source_node))
    if source_node in candidates:
        candidates.remove(source_node)
    set_neighbors(source_node, set())

    distance_to_source_node_fn = lambda p: distance(p, source_node)
    while candidates:
        p_star = min(candidates, key=distance_to_source_node_fn)
        new_neighbors = neighbors(source_node)
        new_neighbors.add(p_star)

        set_neighbors(source_node, new_neighbors)
        if len(new_neighbors) == R:
            break

        to_remove = set()
        for other in candidates:
            if alpha * distance(p_star, other) <= distance(source_node, other):
                to_remove.add(other)
        for node in to_remove:
            candidates.remove(node)

def mediod(points):
    """Returns the mediod of the list of points"""
    medioid = None
    minimum = float('inf')
    for point in points:
        for other in points:
            if point.idx != other.idx:
                d = distance(point, other)
                if d < minimum:
                    minimum = d
                    medioid = point
    return medioid


def distance(p, q):
   """Distance between two nodes p and q."""
   assert(p.vector.size == q.vector.size)
   size = p.vector.size
   total = 0.0
   for i in range(size):
       total += (p.vector[i] - q.vector[i]) * (p.vector[i] - q.vector[i])
   return np.sqrt(total)
    
def neighbors(p):
    """Neighbors of node p in graph rturned as a set."""
    return set(p.outgoing)

def set_neighbors(p, neighbors):
    """Sets the neighbors of node p in the graph."""
    p.outgoing = [other for other in neighbors if p.idx != other.idx]


class Point:
    def __init__(self, idx, vector):
        """
        Represents a point that encapsulates the vector values in a graph.
        """
        self.idx = idx  # Unique identifier of the point.
        self.vector = vector  # Vector data contained by this node. 
        self.outgoing = []  # References to other points this node points to.

    def __hash__(self):
        return self.idx
    
    def add_outgoing_edge(self, point):
        self.outgoing.append(point)



def generate_points(N, dim, bounds):
    """
    Generate a list on N point vectors with dim dimenions.
    """
    points = []
    for i in range(N):
        random_array = np.random.randint(bounds[0], bounds[1], size=dim)
        point = Point(i, random_array)
        points.append(point)
    return points


def generate_graph_edges(points, R):
    size = len(points)
    for i in range(len(points)):
        point = points[i]
        num_of_edges = R

        neighbors = set()
        while len(neighbors) < num_of_edges:
            j = random.randint(0, size - 1)
            neighbors.add(j)
            if point.idx in neighbors:
                neighbors.remove(point.idx)

        for j in neighbors:
            point.add_outgoing_edge(points[j])


def plot_graph(points, name):
    G = nx.Graph()

    for point in points:
        G.add_node(point.idx, vector=point.vector)
    for point in points:
        edges = [[point.idx, other.idx, distance(point, other)] for other in point.outgoing]
        G.add_weighted_edges_from(edges)

    global_custering = nx.average_clustering(G)
    print(f'Clustering co-efficient for graph {name} is: ', global_custering)

    plt.figure(figsize=(80, 80))
    nx.draw(G, 
        pos=nx.spring_layout(G, k=0.15, iterations=20), 
        node_size=20,
        node_color="black"
    )

    plt.plot()
    plt.savefig(name)




def Main(params):
    N = params['N']
    R = params['R']
    L = params['L']

    alpha = params['alpha']
    dimensions = params['dimensions']
    size = params['size']

    # Create list of random points with 2 dimenions
    points = generate_points(N, dimensions, [0, size])
    # Create upto R outgoing links for each point
    generate_graph_edges(points, R)
    # Visualize graph
    plot_graph(points, 'original.png')

    print('Running Vamana with alpha 1')
    vamana_index(points, 1, L, R)

    R = min(R, math.floor(math.log(N)))
    print('Updated R to: ', R)
    
    print('Running Vamana with alpha:', alpha)
    vamana_index(points, alpha, L, R)
    plot_graph(points, 'vamana.png')

    print('Done')


if __name__ == "__main__":
    Main({
        'N': 200,
        'R': 17,
        'L': 10,
        'alpha': 2,
        'dimensions': 8,
        'size': 500
    })