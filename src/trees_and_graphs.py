from typing import Iterable


class Node:
    def __init__(self, data):
        self.data = data
        self._neighbors: set["Node"] = set()

    def __repr__(self) -> str:
        neighbors = ", ".join(
            str(neighbor.data) for neighbor in self._neighbors
        )
        return str(self.data) + (f" -> {neighbors}" if neighbors else "")

    @property
    def neighbors(self):
        return self._neighbors.copy()

    def add_neighbor(self, neighbor: "Node", graph: "Graph") -> None:
        self._neighbors.add(neighbor)
        graph.add(neighbor)

    def remove_neighbor(self, neighbor: "Node") -> None:
        self._neighbors.discard(neighbor)

    def points_to(self, other: "Node") -> bool:
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
