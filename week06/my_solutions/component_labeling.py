from __future__ import annotations
import random

def create_random_undirected_graph(
    n: int, prob: float, no_edge: int, max_edge_wait: int
) -> list[list[int]]:
    g = [[no_edge for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < prob:
                this_edge = (
                    max_edge_wait
                    if max_edge_wait == 1
                    else random.randint(1, max_edge_wait)
                )
                g[i][j] = this_edge
                g[j][i] = this_edge
    return g

def reached(starting_vertex: int, g: list[list[int]]) -> list[int]:
    visited: list[int] = []  # vertices already explored
    gonext: list[int] = [starting_vertex]  # worklist, seeded with the start
    while len(gonext) > 0:
        u = gonext.pop()  # LIFO: explore the most recently found vertex next
        if u not in visited:
            visited.append(u)
            # row u of the adjacency matrix lists u's neighbors
            for v in range(len(g)):
                if g[u][v] != 0 and v not in visited:
                    gonext.append(v)  # found a new vertex to explore
    return visited


def count_components(g: list[list[int]]) -> int:
    components: int = 0
    marked: list[int] = []  # vertices already swept into some component
    for starting_vertex in range(len(g)):
        if starting_vertex not in marked:
            components += 1
            marked.extend(reached(starting_vertex, g))
    return components

def label_components(g: list[list[int]]) -> list[int]:
    labels = [-1] * len(g)
    current_label = 0
    for starting_vertex in range(len(g)):
        if labels[starting_vertex] == -1:
            for v in reached(starting_vertex, g):
                labels[v] = current_label
            current_label += 1
    return labels

def connected(u: int, v: int, g: list[list[int]], labels: list[int] | None = None) -> bool:
    if labels is None:
        labels = label_components(g)
    return labels[u] == labels[v]

def largest_component(g: list[list[int]]) -> tuple[int, list[int]]:
    labels = label_components(g)
    biggest = max(set(labels), key=labels.count)
    vertices = [v for v in range(len(g)) if labels[v] == biggest]
    return len(vertices), vertices

def from_edges(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """build an n x n adjacency matrix from a list of undirected edges"""
    g = [[0] * n for _ in range(n)]
    for i, j in edges:
        g[i][j] = 1
        g[j][i] = 1
    return g


def grouping(labels: list[int]) -> list[list[int]]:
    """turn a labels list into a sorted list of vertex groups"""
    groups = []
    for label in set(labels):
        groups.append([v for v in range(len(labels)) if labels[v] == label])
    return sorted(groups)


CLASS_EXAMPLE = from_edges(6, [(0, 1), (0, 2), (3, 4)])
NO_EDGES = from_edges(4, [])
K4_COMPLETE = from_edges(4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
TWO_TRIANGLES = from_edges(6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5)])
PATH = from_edges(5, [(0, 1), (1, 2), (2, 3), (3, 4)])


def run_checks() -> None:
    # label_components, each graph splits into the right groups
    assert grouping(label_components(CLASS_EXAMPLE)) == [[0, 1, 2], [3, 4], [5]]
    assert grouping(label_components(NO_EDGES)) == [[0], [1], [2], [3]]
    assert grouping(label_components(K4_COMPLETE)) == [[0, 1, 2, 3]]
    assert grouping(label_components(TWO_TRIANGLES)) == [[0, 1, 2], [3, 4, 5]]
    assert grouping(label_components(PATH)) == [[0, 1, 2, 3, 4]]

    # check largest_component on normal graph and triangle
    assert largest_component(CLASS_EXAMPLE)[0] == 3
    assert largest_component(TWO_TRIANGLES)[0] == 3

    # yes/no on specific pairs
    labels = label_components(CLASS_EXAMPLE)
    assert connected(1, 2, CLASS_EXAMPLE, labels)
    assert not connected(2, 3, CLASS_EXAMPLE, labels)
    assert not connected(4, 5, CLASS_EXAMPLE, labels)
    assert connected(1, 2, CLASS_EXAMPLE)

    # Random graphs, distinct labels must match count_components
    for _ in range(5):
        g = create_random_undirected_graph(12, 0.15, 0, 1)
        assert len(set(label_components(g))) == count_components(g)

    print("All checks passed")


if __name__ == "__main__":
    run_checks()
