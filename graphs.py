"""
Random Graph Generation Algorithms

Python implementation of classical random graph models.
Includes Erdős–Rényi random graphs and Galton–Watson branching processes.
"""

from typing import List, Dict, Tuple
import numpy as np
from collections import deque
import math


class Graph:
    """
    Simple undirected graph.

    Attributes:
        n_nodes: Number of nodes in the graph
        edges: List of edges as (u, v) pairs
        adjacency: Adjacency list for each node
    """

    def __init__(self, n_nodes: int) -> None:
        """Initialize an empty graph with n_nodes vertices."""
        self.n_nodes = n_nodes
        self.edges: List[Tuple[int, int]] = []
        self.adjacency: List[List[int]] = [[] for _ in range(n_nodes)]

    def add_edge(self, u: int, v: int) -> None:
        """Add an undirected edge between nodes u and v."""
        if u != v and v not in self.adjacency[u]:
            self.edges.append((u, v))
            self.adjacency[u].append(v)
            self.adjacency[v].append(u)

    def get_edges(self) -> List[Tuple[int, int]]:
        """Return all edges in the graph."""
        return self.edges

    def get_neighbors(self, node: int) -> List[int]:
        """Return neighbors of a given node."""
        return self.adjacency[node]

    def degree(self, node: int) -> int:
        """Return the degree of a node."""
        return len(self.adjacency[node])

    def number_of_edges(self) -> int:
        """Return total number of edges in the graph."""
        return len(self.edges)


class Tree:
    """
    Simple directed tree for branching processes.

    Attributes:
        nodes: List of node IDs
        edges: List of parent-child edges
        children: Children of each node
        parents: Parent of each node
        levels: Generation/level of each node
    """

    def __init__(self) -> None:
        """Initialize an empty tree."""
        self.nodes: List[int] = []
        self.edges: List[Tuple[int, int]] = []
        self.children: Dict[int, List[int]] = {}
        self.parents: Dict[int, int] = {}
        self.levels: Dict[int, int] = {}

    def add_node(self, node_id: int, level: int = 0) -> None:
        """Add a node to the tree with its generation level."""
        self.nodes.append(node_id)
        self.children[node_id] = []
        self.levels[node_id] = level

    def add_edge(self, parent: int, child: int) -> None:
        """Add a parent-child edge to the tree."""
        self.edges.append((parent, child))
        if parent not in self.children:
            self.children[parent] = []
        self.children[parent].append(child)
        self.parents[child] = parent

    def get_leaves(self) -> List[int]:
        """Return all leaf nodes (nodes with no children)."""
        return [node for node in self.nodes if len(self.children.get(node, [])) == 0]

    def total_population(self) -> int:
        """Return total number of nodes in the tree."""
        return len(self.nodes)


def generate_erdos_renyi(n: int, p: float) -> Graph:
    """
    Generate an Erdős–Rényi random graph G(n, p).

    Each possible edge is added independently with probability p.

    Args:
        n: Number of nodes
        p: Edge probability (0 <= p <= 1)

    Returns:
        Random graph instance
    """
    if not (0 <= p <= 1):
        raise ValueError(f"Edge probability must be between 0 and 1, got {p}")
    if n < 0:
        raise ValueError(f"Number of nodes must be non-negative, got {n}")

    graph = Graph(n)

    # Attempt to add each possible edge independently
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.random() < p:
                graph.add_edge(i, j)

    return graph


def generate_circular_positions(n: int, radius: float = 1.0) -> Dict[int, Tuple[float, float]]:
    """
    Generate positions for nodes on a circle.

    Args:
        n: Number of nodes
        radius: Circle radius

    Returns:
        Dictionary mapping node ID to (x, y) position
    """
    positions = {}
    for i in range(n):
        angle = 2 * np.pi * i / n if n > 0 else 0
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        positions[i] = (x, y)
    return positions


def generate_spring_positions(
    graph: Graph, 
    iterations: int = 50, 
    k: float = 1.0,
    initial_temp: float = 1.0
) -> Dict[int, Tuple[float, float]]:
    """
    Force-directed layout for graph visualization.

    Uses repulsive forces between all nodes and attractive forces along edges.

    Args:
        graph: Graph to layout
        iterations: Number of iterations
        k: Spring constant
        initial_temp: Initial temperature for annealing

    Returns:
        Node positions as a dictionary {node: (x, y)}
    """
    n = graph.n_nodes
    if n == 0:
        return {}

    positions = {i: (np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for i in range(n)}

    for iteration in range(iterations):
        temp = initial_temp * (1 - iteration / iterations)  # Cooling schedule
        forces = {i: [0.0, 0.0] for i in range(n)}

        # Repulsive forces between all node pairs
        for i in range(n):
            for j in range(i + 1, n):
                dx = positions[i][0] - positions[j][0]
                dy = positions[i][1] - positions[j][1]
                dist = max(math.sqrt(dx*dx + dy*dy), 0.01)
                force = k * k / (dist * dist)
                fx = force * dx / dist
                fy = force * dy / dist
                forces[i][0] += fx
                forces[i][1] += fy
                forces[j][0] -= fx
                forces[j][1] -= fy

        # Attractive forces along edges
        for u, v in graph.get_edges():
            dx = positions[u][0] - positions[v][0]
            dy = positions[u][1] - positions[v][1]
            dist = max(math.sqrt(dx*dx + dy*dy), 0.01)
            force = dist / k
            fx = force * dx / dist
            fy = force * dy / dist
            forces[u][0] -= fx
            forces[u][1] -= fy
            forces[v][0] += fx
            forces[v][1] += fy

        # Update positions
        step_size = 0.1 * temp
        for i in range(n):
            positions[i] = (
                positions[i][0] + forces[i][0] * step_size,
                positions[i][1] + forces[i][1] * step_size
            )

    return positions


def generate_galton_watson_tree(lam: float, max_generations: int) -> Tuple[Tree, bool, list]:
    """
    Generate a Galton–Watson branching tree.

    Each node produces a Poisson(lam) number of children independently.
    The process stops either when extinction occurs or when the maximum
    number of generations is reached (truncated tree).

    Args:
        lam: Poisson parameter (expected number of children per node)
        max_generations: Maximum number of generations to simulate

    Returns:
        tree: Generated Tree object
        reached_max: True if max_generations was reached while nodes were still alive
        sizes_per_generation: List of node counts per generation
    """
   
    if lam <= 0:
        raise ValueError(f"Poisson parameter must be positive, got {lam}")
    if max_generations <= 0:
        raise ValueError(f"Maximum generations must be positive, got {max_generations}")

    tree = Tree()
    tree.add_node(0, level=0)  # Root node
    current_generation = [0]
    node_counter = 1
    generation = 0
    reached_max = False
    sizes_per_generation = [1]  # Include root

    while current_generation and generation < max_generations:
        next_generation = []
        generation += 1

        for parent in current_generation:
            num_offspring = np.random.poisson(lam)
            for _ in range(num_offspring):
                child_id = node_counter
                tree.add_node(child_id, level=generation)
                tree.add_edge(parent, child_id)
                next_generation.append(child_id)
                node_counter += 1

        current_generation = next_generation
        sizes_per_generation.append(len(current_generation))

        if generation == max_generations and current_generation:
            reached_max = True

    return tree, reached_max, sizes_per_generation