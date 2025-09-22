"""
Minimalistic Graph Visualization

Unified color scheme for Erdős–Rényi and Galton–Watson graphs.
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from graphs import generate_erdos_renyi, generate_galton_watson_tree, generate_circular_positions

COLOR_PARENT = "#E74C3C"   # nodes with children
COLOR_LEAF = "#3498DB"     # isolated or leaf nodes
COLOR_ROOT = "#8E44AD"     # root node (special color)
COLOR_EDGE = "#333333"     # edges (bolder)
NODE_SIZE = 40


class ErdosRenyi:
    """Visualize Erdős–Rényi graphs."""

    def __init__(self, n, p):
        self.n = n
        self.p = p
        plt.style.use("default")
        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.patch.set_facecolor("white")
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.refresh_graph()

    def draw_graph(self):
        self.ax.clear()
        self.ax.set_facecolor("white")
        graph = generate_erdos_renyi(self.n, self.p)
        if graph.n_nodes == 0:
            self.ax.text(0.5, 0.5, "Empty", ha="center", va="center",
                         transform=self.ax.transAxes, fontsize=16, color="gray")
            return

        positions = generate_circular_positions(graph.n_nodes, radius=0.8)
        connected = set(u for edge in graph.get_edges() for u in edge)
        isolated = set(range(graph.n_nodes)) - connected

        for u, v in graph.get_edges():
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            self.ax.plot([x1, x2], [y1, y2], color=COLOR_EDGE, linewidth=1.2, alpha=0.7)

        if connected:
            x, y = zip(*[positions[n] for n in connected])
            self.ax.scatter(x, y, c=COLOR_PARENT, s=NODE_SIZE, zorder=2)
        if isolated:
            x, y = zip(*[positions[n] for n in isolated])
            self.ax.scatter(x, y, c=COLOR_LEAF, s=NODE_SIZE, zorder=2)

        self.ax.set_xlim(-1.2, 1.2)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

    def refresh_graph(self):
        self.draw_graph()
        self.fig.suptitle(f"Erdős–Rényi G({self.n}, {self.p:.3f})",
                          fontsize=14, color="#2C3E50", y=0.95)
        plt.tight_layout()
        plt.draw()

    def on_click(self, event):
        self.refresh_graph()

    def show(self):
        plt.show()


class GaltonWatson:
    """Visualize Galton–Watson trees in radial layout."""

    def __init__(self, lam, max_gen, outer_radius=1.0):
        self.lam = lam
        self.max_gen = max_gen
        self.outer_radius = outer_radius
        plt.style.use("default")
        self.fig, self.ax = plt.subplots(figsize=(9, 8))
        self.fig.patch.set_facecolor("white")
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.refresh_tree()

    def compute_radial_layout(self, tree, root=0):
        if not tree.nodes:
            return {}
        max_level = max(tree.levels.values()) if tree.levels else 0

        def collect_leaves(node):
            children = tree.children.get(node, [])
            if not children:
                return [node]
            leaves = []
            for c in children:
                leaves.extend(collect_leaves(c))
            return leaves

        leaves = collect_leaves(root)
        n_leaves = len(leaves)
        leaf_angles = {leaf: 2*math.pi*i/n_leaves for i, leaf in enumerate(leaves)}
        pos, span = {}, {}

        def assign_spans(node):
            children = tree.children.get(node, [])
            if not children:
                span[node] = (leaf_angles[node], leaf_angles[node])
                return span[node]
            child_spans = [assign_spans(c) for c in children]
            a_min = min(s[0] for s in child_spans)
            a_max = max(s[1] for s in child_spans)
            if a_max - a_min > math.pi:
                unwrapped = [(s0+2*math.pi if s0<math.pi else s0, s1+2*math.pi if s1<math.pi else s1)
                             for s0, s1 in child_spans]
                a_min = min(s[0] for s in unwrapped)
                a_max = max(s[1] for s in unwrapped)
                span[node] = (a_min % (2*math.pi), a_max % (2*math.pi))
            else:
                span[node] = (a_min, a_max)
            return span[node]

        assign_spans(root)

        for node in tree.nodes:
            a_min, a_max = span[node]
            mid_angle = (a_min + (a_max-a_min) % (2*math.pi)/2) % (2*math.pi)
            depth = tree.levels.get(node, 0)
            min_r = 0.0 if node==root else 0.08*self.outer_radius
            r = min_r + (depth/max(1,max_level))*(self.outer_radius - min_r)
            pos[node] = (r*math.cos(mid_angle), r*math.sin(mid_angle))
        return pos

    def draw_tree(self, tree, truncated=False):
        self.ax.clear()
        self.ax.set_facecolor("white")
        if not tree.nodes:
            self.ax.text(0.5, 0.5, "Extinct", ha="center", va="center",
                         transform=self.ax.transAxes, fontsize=16, color="gray")
            return

        positions = self.compute_radial_layout(tree)
        for parent, child in tree.edges:
            if parent in positions and child in positions:
                px, py = positions[parent]
                cx, cy = positions[child]
                self.ax.plot([px, cx], [py, cy], color=COLOR_EDGE, linewidth=1.5, alpha=0.8)

        parents = {p for p,_ in tree.edges}
        leaves = [n for n in tree.nodes if len(tree.children.get(n, []))==0]

        # Draw root node with special color and style
        root = 0
        if root in positions:
            rx, ry = positions[root]
            self.ax.scatter([rx], [ry], c=COLOR_ROOT, s=NODE_SIZE + 15, zorder=3,
                          edgecolors='white', linewidths=2)

        # Draw other parent nodes (excluding root)
        other_parents = parents - {root}
        if other_parents:
            x, y = zip(*[positions[n] for n in other_parents if n in positions])
            self.ax.scatter(x, y, c=COLOR_PARENT, s=NODE_SIZE, zorder=2)

        # Draw leaf nodes
        if leaves:
            x, y = zip(*[positions[n] for n in leaves if n in positions])
            self.ax.scatter(x, y, c=COLOR_LEAF, s=NODE_SIZE, zorder=2)

        pad = 1.2
        self.ax.set_xlim(-pad*self.outer_radius, pad*self.outer_radius)
        self.ax.set_ylim(-pad*self.outer_radius, pad*self.outer_radius)
        self.ax.set_aspect("equal")
        self.ax.axis("off")

        status = f"(truncated with {self.max_gen} gens)" if truncated else "(extinct)"
        self.fig.suptitle(f"Galton–Watson λ={self.lam:.2f} {status}",
                          fontsize=14, color="#2C3E50", y=0.95)
        plt.tight_layout()
        plt.draw()

    def refresh_tree(self):
        tree, reached_max, sizes_per_generation = generate_galton_watson_tree(self.lam, self.max_gen)
        truncated = reached_max and len(tree.nodes) > 0
        self.draw_tree(tree, truncated=truncated)

    def on_click(self, event):
        self.refresh_tree()

    def show(self):
        plt.show()


def visualize_erdos_renyi(n, p):
    ErdosRenyi(n, p).show()


def visualize_galton_watson(lam, max_gen):
    GaltonWatson(lam, max_gen).show()