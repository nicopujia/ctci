from src.trees_and_graphs import (
    Graph,
    Node,
    UndirectedGraph,
    UndirectedNode,
    check_route,
)


class TestGraphAndNode:
    def setup_method(self):
        self.n = [Node(i) for i in range(5)]
        self.g = Graph(self.n)

    def test_nodes_data(self):
        for i in range(len(self.n)):
            assert self.n[i].data == i

    def test_no_neighbors_initially(self):
        for node in self.n:
            assert len(node.neighbors) == 0

    def test_connect_one_to_itself(self):
        self.g.connect(self.n[0], self.n[0])
        assert self.g.are_connected(self.n[0], self.n[0])

    def test_connect_one_to_another_in_one_way(self):
        self.g.connect(self.n[0], self.n[1])
        assert self.n[0].points_to(self.n[1])
        assert not self.n[1].points_to(self.n[0])

    def test_connect_same_nodes_multiple_times_keeps_one_connection(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[1])
        assert len(self.n[0].neighbors) == 1

    def test_connect_one_to_another_in_both_ways(self):
        self.g.connect(self.n[0], self.n[1], both_ways=True)
        assert self.g.are_connected(self.n[0], self.n[1], both_ways=True)

    def test_connect_one_to_many_in_one_way(self):
        for i in range(1, 5):
            self.g.connect(self.n[0], self.n[i])
        for i in range(1, 5):
            assert self.n[0].points_to(self.n[i])
            assert not self.n[i].points_to(self.n[0])

    def test_connect_one_to_many_in_both_ways(self):
        for i in range(1, 5):
            self.g.connect(self.n[0], self.n[i], both_ways=True)
        for i in range(1, 5):
            assert self.g.are_connected(self.n[0], self.n[i], both_ways=True)

    def test_connect_one_to_many_and_one_of_them_to_the_other(self):
        for i in range(1, 4):
            self.g.connect(self.n[0], self.n[i])
        self.g.connect(self.n[1], self.n[2])
        for i in range(1, 4):
            assert self.n[0].points_to(self.n[i])
            assert not self.n[i].points_to(self.n[0])
        assert self.n[1].points_to(self.n[2])
        assert not self.n[2].points_to(self.n[1])

    def test_connect_many_to_one_in_one_way(self):
        for i in range(1, 5):
            self.g.connect(self.n[i], self.n[0])
        for i in range(1, 5):
            assert self.n[i].points_to(self.n[0])
            assert not self.n[0].points_to(self.n[i])

    def test_connect_many_in_one_way_with_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.connect(self.n[4], self.n[0])
        for i in range(4):
            assert self.n[i].points_to(self.n[i + 1])
        assert self.n[4].points_to(self.n[0])

    def test_connect_many_in_one_way_without_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        for i in range(4):
            assert self.n[i].points_to(self.n[i + 1])
        assert not self.n[4].points_to(self.n[0])

    def test_connect_many_in_both_ways_with_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1], both_ways=True)
        self.g.connect(self.n[4], self.n[0], both_ways=True)
        for i in range(4):
            assert self.g.are_connected(
                self.n[i], self.n[i + 1], both_ways=True
            )
        assert self.g.are_connected(self.n[4], self.n[0], both_ways=True)

    def test_connect_many_in_both_ways_without_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1], both_ways=True)
        for i in range(4):
            assert self.g.are_connected(
                self.n[i], self.n[i + 1], both_ways=True
            )
        assert not self.g.are_connected(self.n[4], self.n[0])
        assert not self.g.are_connected(self.n[0], self.n[4])

    def test_connect_many_to_many_in_both_ways(self):
        for i in range(5):
            for j in range(5):
                if i != j:
                    self.g.connect(self.n[i], self.n[j], both_ways=True)
        for i in range(5):
            for j in range(5):
                if i != j:
                    assert self.g.are_connected(
                        self.n[i], self.n[j], both_ways=True
                    )

    def test_disconnect_disconnected_nodes_does_nothing(self):
        assert not self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1])
        assert not self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1], both_ways=True)
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_disconnect_connected_nodes_in_one_way(self):
        self.g.connect(self.n[0], self.n[1])
        assert self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[1], self.n[0])
        assert self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1])
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_disconnect_connected_nodes_in_both_ways(self):
        self.g.connect(self.n[0], self.n[1], both_ways=True)
        self.g.disconnect(self.n[1], self.n[0], both_ways=True)
        assert not self.g.are_connected(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[1], both_ways=True)
        self.g.disconnect(self.n[0], self.n[1], both_ways=True)
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_remove_node_without_connections(self):
        self.g.remove(self.n[0])
        assert self.n[0] not in self.g.nodes

    def test_remove_node_with_connections(self):
        for i in range(2):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.remove(self.n[1])
        assert self.n[0] in self.g.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[2] in self.g.nodes
        for i in range(3):
            assert not self.n[i].neighbors

    def test_remove_node_with_connections_from_two_graphs(self):
        self.g.connect(self.n[0], self.n[1], both_ways=True)
        g2_node = Node(2)
        g2 = Graph([self.n[1], g2_node])
        g2.connect(self.n[1], g2_node, both_ways=True)
        # At this point we have two graphs like this: [n0 <-> (n1] <-> g2_node)
        self.g.remove(self.n[1])
        assert g2_node in g2.nodes
        assert self.n[1] in g2.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[0] in self.g.nodes
        assert g2.are_connected(self.n[1], g2_node, both_ways=True)
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_graph_repr_with_nodes(self):
        assert repr(self.g) == "Graph(5 nodes)"

    def test_graph_repr_without_nodes(self):
        assert repr(Graph()) == "Graph(0 nodes)"

    def test_graph_repr_with_one_node(self):
        g = Graph()
        g.add(Node(10))
        assert repr(g) == "Graph(1 node)"

    def test_node_repr_with_number(self):
        assert repr(self.n[0]) == "Node(0)"

    def test_node_repr_with_non_empty_string(self):
        assert repr(Node("hello world")) == "Node('hello world')"

    def test_node_repr_with_empty_string(self):
        assert repr(Node("")) == "Node('')"

    def test_node_str_without_connections(self):
        assert str(self.n[0]) == "0"

    def test_node_str_with_connection_by_other(self):
        self.g.connect(self.n[1], self.n[0])
        assert str(self.n[0]) == "0"

    def test_node_str_with_one_neighbor(self):
        self.g.connect(self.n[0], self.n[1])
        assert str(self.n[0]) == "0 -> {1}"

    def test_node_str_with_multiple_neighbors(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[2])
        # Because sets are unordered data structures, the neighbors may appear
        # in different order in different runs.
        assert str(self.n[0]) in ("0 -> {1, 2}", "0 -> {2, 1}")


class TestUndirectedGraphAndItsNode:
    def setup_method(self):
        self.n = [UndirectedNode(i) for i in range(5)]
        self.g = UndirectedGraph(self.n)

    def test_nodes_data(self):
        for i in range(len(self.n)):
            assert self.n[i].data == i

    def test_no_neighbors_initially(self):
        for node in self.n:
            assert len(node.neighbors) == 0

    def test_connect_one_to_itself(self):
        self.g.connect(self.n[0], self.n[0])
        assert self.g.are_connected(self.n[0], self.n[0])

    def test_connect_one_to_another(self):
        self.g.connect(self.n[0], self.n[1])
        assert self.g.are_connected(self.n[0], self.n[1])

    def test_connect_same_nodes_multiple_times_keeps_one_connection(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[1])
        assert len(self.n[0].neighbors) == 1

    def test_connect_one_with_many(self):
        for i in range(1, 5):
            self.g.connect(self.n[0], self.n[i])
        for i in range(1, 5):
            assert self.g.are_connected(self.n[0], self.n[i])

    def test_connect_one_to_many_and_one_of_them_to_the_other(self):
        for i in range(1, 4):
            self.g.connect(self.n[0], self.n[i])
        self.g.connect(self.n[1], self.n[2])
        for i in range(1, 4):
            assert self.g.are_connected(self.n[0], self.n[i])
        assert self.g.are_connected(self.n[1], self.n[2])

    def test_connect_many_with_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.connect(self.n[4], self.n[0])
        for i in range(4):
            assert self.g.are_connected(self.n[i], self.n[i + 1])
        assert self.g.are_connected(self.n[4], self.n[0])

    def test_connect_many_without_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        for i in range(4):
            assert self.g.are_connected(self.n[i], self.n[i + 1])
        assert not self.g.are_connected(self.n[0], self.n[4])

    def test_connect_many_with_many(self):
        for i in range(5):
            for j in range(5):
                if i != j:
                    self.g.connect(self.n[i], self.n[j])
        for i in range(5):
            for j in range(5):
                if i != j:
                    assert self.g.are_connected(self.n[i], self.n[j])

    def test_disconnect_disconnected_nodes_does_nothing(self):
        assert not self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1])
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_disconnect_connected_nodes(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.disconnect(self.n[1], self.n[0])
        assert not self.g.are_connected(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1])
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_remove_node_without_connections(self):
        self.g.remove(self.n[0])
        assert self.n[0] not in self.g.nodes

    def test_remove_node_with_connections(self):
        for i in range(2):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.remove(self.n[1])
        assert self.n[0] in self.g.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[2] in self.g.nodes
        for i in range(3):
            assert not self.n[i].neighbors

    def test_remove_node_with_connections_from_two_graphs(self):
        self.g.connect(self.n[0], self.n[1])
        g2_node = UndirectedNode(2)
        g2 = UndirectedGraph([self.n[1], g2_node])
        g2.connect(self.n[1], g2_node)
        # At this point we have two graphs like this: [n0 <-> (n1] <-> g2_node)
        self.g.remove(self.n[1])
        assert g2_node in g2.nodes
        assert self.n[1] in g2.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[0] in self.g.nodes
        assert g2.are_connected(self.n[1], g2_node)
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_graph_repr_with_nodes(self):
        assert repr(self.g) == "UndirectedGraph(5 nodes)"

    def test_graph_repr_without_nodes(self):
        assert repr(UndirectedGraph()) == "UndirectedGraph(0 nodes)"

    def test_graph_repr_with_one_node(self):
        g = UndirectedGraph()
        g.add(UndirectedNode(10))
        assert repr(g) == "UndirectedGraph(1 node)"

    def test_node_repr_with_number(self):
        assert repr(self.n[0]) == "UndirectedNode(0)"

    def test_node_repr_with_non_empty_string(self):
        assert repr(UndirectedNode("hello")) == "UndirectedNode('hello')"

    def test_node_repr_with_empty_string(self):
        assert repr(UndirectedNode("")) == "UndirectedNode('')"

    def test_node_str_without_connections(self):
        assert str(self.n[0]) == "0"

    def test_node_str_with_connection_by_other(self):
        self.g.connect(self.n[1], self.n[0])
        assert str(self.n[0]) == "0 -> {1}"

    def test_node_str_with_one_neighbor(self):
        self.g.connect(self.n[0], self.n[1])
        assert str(self.n[0]) == "0 -> {1}"

    def test_node_str_with_multiple_neighbors(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[2])
        # Because sets are unordered data structures, the neighbors may appear
        # in different order in different runs.
        assert str(self.n[0]) in ("0 -> {1, 2}", "0 -> {2, 1}")


class TestCheckRoute:
    def setup_method(self):
        self.g = Graph()

    def test_one_node(self):
        n = Node(1)
        self.g.add(n)
        assert not check_route(n, n)

    def test_one_node_connected_to_itself(self):
        n = Node(1)
        self.g.add(n)
        self.g.connect(n, n)
        assert check_route(n, n)

    def test_two_nodes_connected_in_one_way(self):
        a, b = Node("a"), Node("b")
        self.g.add(a, b)
        self.g.connect(a, b)
        assert check_route(a, b)

    def test_two_nodes_connected_in_the_other_way(self):
        a, b = Node("a"), Node("b")
        self.g.add(a, b)
        self.g.connect(b, a)
        assert not check_route(a, b)

    def test_two_nodes_connected_in_both_ways(self):
        a, b = Node("a"), Node("b")
        self.g.add(a, b)
        self.g.connect(a, b, both_ways=True)
        assert check_route(a, b)

    def test_two_disconnected_nodes(self):
        a, b = Node("a"), Node("b")
        self.g.add(a, b)
        assert not check_route(a, b)

    def test_three_nodes_connected_in_one_way(self):
        a, middle, b = Node("a"), Node(1), Node("b")
        self.g.add(a, middle, b)
        self.g.connect(a, middle)
        self.g.connect(middle, b)
        assert check_route(a, b)

    def test_three_nodes_with_end_nodes_pointing_to_middle_node(self):
        a, middle, b = Node("a"), Node(1), Node("b")
        self.g.add(a, middle, b)
        self.g.connect(a, middle)
        self.g.connect(b, middle)
        assert not check_route(a, b)

    def test_multiple_routes_with_only_one_correct(self):
        a, b = Node("a"), Node("b")
        wrong, wrong_2 = Node(10), Node(20)
        correct, correct_2, correct_3 = Node(1), Node(2), Node(3)
        self.g.add(a, wrong, wrong_2, correct, correct_2, correct_3, b)
        self.g.connect(a, wrong)
        self.g.connect(wrong, wrong_2)
        self.g.connect(a, correct)
        self.g.connect(correct, correct_2)
        self.g.connect(correct_2, correct_3)
        self.g.connect(correct_3, b)
        assert check_route(a, b)

    def test_multiple_nodes_in_between(self):
        nodes = [Node(i) for i in range(10)]
        self.g.add(*nodes)
        for i in range(len(nodes) - 1):
            self.g.connect(nodes[i], nodes[i + 1], both_ways=True)
        assert check_route(nodes[0], nodes[-1])

    def test_loop_with_correct_path(self):
        a, middle, b = Node("a"), Node(1), Node("b")
        self.g.add(a, middle, b)
        self.g.connect(a, middle)
        self.g.connect(middle, b)
        self.g.connect(b, a)
        assert check_route(a, b)

    def test_loop_without_correct_route(self):
        a, loop_1, loop_2, b = Node("a"), Node(1), Node(2), Node("b")
        self.g.add(a, loop_1, loop_2, b)
        self.g.connect(a, loop_1)
        self.g.connect(loop_1, loop_2)
        self.g.connect(loop_2, a)
        assert not check_route(a, b)
