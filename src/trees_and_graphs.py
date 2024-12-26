from typing import Iterable, Self


class Node:
    def __init__(self, data):
        self.data = data
        self.visited = False
        self._neighbors: set[Self] = set()

    def __repr__(self) -> str:
        return "Node(%s)" % repr(self.data)

    def __str__(self) -> str:
        neighbors = ", ".join(
            str(neighbor.data) for neighbor in self._neighbors
        )
        return str(self.data) + (" -> {%s}" % neighbors if neighbors else "")

    @property
    def neighbors(self):
        return self._neighbors.copy()

    def add_neighbor(self, neighbor: Self, graph: "Graph") -> None:
        self._neighbors.add(neighbor)
        graph.add(neighbor)

    def remove_neighbor(self, neighbor: Self) -> None:
        self._neighbors.discard(neighbor)

    def points_to(self, other: Self) -> bool:
        return other in self._neighbors


class Graph:
    def __init__(self, nodes: Iterable[Node] = set()):
        self._nodes = set(nodes)

    def __repr__(self) -> str:
        nodes_count = len(self._nodes)
        nodes_plural = "s" if len(self._nodes) != 1 else ""
        return f"Graph({nodes_count} node{nodes_plural})"

    @property
    def nodes(self):
        return self._nodes.copy()

    def add(self, *nodes: Node) -> None:
        self._nodes.update(nodes)

    def remove(self, node: Node) -> None:
        self._nodes.discard(node)
        for other_node in self._nodes:
            self.disconnect(node, other_node, both_ways=True)

    def connect(self, a: Node, b: Node, both_ways: bool = False) -> None:
        a.add_neighbor(b, self)
        if both_ways:
            self.connect(b, a)

    def disconnect(self, a: Node, b: Node, both_ways: bool = False) -> None:
        a.remove_neighbor(b)
        if both_ways:
            self.disconnect(b, a)

    def are_connected(self, a: Node, b: Node, both_ways: bool = False) -> bool:
        if both_ways:
            return a in b.neighbors and b in a.neighbors
        return a in b.neighbors or b in a.neighbors


def check_route(a: Node, b: Node) -> bool:
    """Return whether or not there is a route between nodes `a` and `b`."""
    neighbors = a.neighbors
    while neighbors:
        previous_neighbors = neighbors.copy()
        for neighbor in neighbors:
            if neighbor is b:
                return True
            neighbor.visited = True
        neighbors.clear()
        for previous_neighbor in previous_neighbors:
            unvisited_neighbors = filter(
                lambda node: not node.visited,
                previous_neighbor.neighbors,
            )
            neighbors.update(unvisited_neighbors)
    return False
