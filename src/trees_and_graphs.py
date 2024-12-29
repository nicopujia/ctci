from typing import Iterable, Self


class Node:
    def __init__(self, data):
        self.data = data
        self.visited = False
        self._neighbors: set[Self] = set()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.data)})"

    def __str__(self) -> str:
        neighbors = ", ".join(
            str(neighbor.data) for neighbor in self._neighbors
        )
        return str(self.data) + (" -> {%s}" % neighbors if neighbors else "")

    @property
    def neighbors(self):
        return self._neighbors.copy()

    def add_neighbor(
        self, neighbor: Self, graph: "Graph", both_ways: bool = False
    ) -> None:
        self._neighbors.add(neighbor)
        graph.add(neighbor, self)
        if both_ways and self not in neighbor.neighbors:
            neighbor.add_neighbor(self, graph)

    def remove_neighbor(self, neighbor: Self, both_ways: bool = False) -> None:
        self._neighbors.discard(neighbor)
        if both_ways and self in neighbor.neighbors:
            neighbor.remove_neighbor(self)

    def points_to(self, other: Self) -> bool:
        return other in self._neighbors


class Graph:
    def __init__(self, nodes: Iterable[Node] = set()):
        self._nodes = set(nodes)

    def __repr__(self) -> str:
        nodes_count = len(self._nodes)
        nodes_plural = "s" if len(self._nodes) != 1 else ""
        return f"{self.__class__.__name__}({nodes_count} node{nodes_plural})"

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
        a.add_neighbor(b, self, both_ways=both_ways)

    def disconnect(self, a: Node, b: Node, both_ways: bool = False) -> None:
        a.remove_neighbor(b, both_ways=both_ways)

    def are_connected(self, a: Node, b: Node, both_ways: bool = False) -> bool:
        if both_ways:
            return a.points_to(b) and b.points_to(a)
        return a.points_to(b) or b.points_to(a)


class UndirectedNode(Node):
    def add_neighbor(self, neighbor: Self, graph: "UndirectedGraph"):
        super().add_neighbor(neighbor, graph, both_ways=True)

    def remove_neighbor(self, neighbor: Self):
        super().remove_neighbor(neighbor, both_ways=True)


class UndirectedGraph(Graph):
    """Graph where all connections are in both ways."""

    def __init__(self, nodes: set[UndirectedNode] = set()):
        super().__init__(nodes)

    def remove(self, node):
        self._nodes.discard(node)
        for other_node in self._nodes:
            self.disconnect(node, other_node)

    def connect(self, a: UndirectedNode, b: UndirectedNode):
        a.add_neighbor(b, self)

    def disconnect(self, a: UndirectedNode, b: UndirectedNode):
        a.remove_neighbor(b)

    def are_connected(self, a: UndirectedNode, b: UndirectedNode):
        return super().are_connected(a, b, both_ways=True)


class TreeNode:
    def __init__(self, data, parent: Self | None = None):
        self.data = data
        self.parent = parent
        self._children = []
        if parent:
            parent.add_child(self)

    def __repr__(self) -> str:
        return f"TreeNode({self.data}" + (
            f", parent={repr(self.parent)})" if self.parent else ")"
        )

    @property
    def children(self):
        return self._children.copy()

    def add_child(self, child: Self) -> None:
        self._children.append(child)
        child.parent = self

    def remove_child(self, child: Self) -> None:
        self._children.remove(child)
        child.parent = None


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
