from src.trees_and_graphs import Graph, Node


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

    def test_connect_one_to_another_in_single_direction(self):
        self.g.connect(self.n[0], self.n[1])
        assert self.n[0].points_to(self.n[1])
        assert not self.n[1].points_to(self.n[0])

    def test_connect_same_nodes_multiple_times_keeps_one_connection(self):
        self.g.connect(self.n[0], self.n[1])
        self.g.connect(self.n[0], self.n[1])
        assert len(self.n[0].neighbors) == 1

    def test_connect_one_to_another_in_both_directions(self):
        self.g.connect(self.n[0], self.n[1], both_ways=True)
        assert self.g.are_connected(self.n[0], self.n[1], both_ways=True)

    def test_connect_one_to_many_single_direction(self):
        for i in range(1, 5):
            self.g.connect(self.n[0], self.n[i])
        for i in range(1, 5):
            assert self.n[0].points_to(self.n[i])
            assert not self.n[i].points_to(self.n[0])

    def test_connect_one_to_many_in_both_directions(self):
        for i in range(1, 5):
            self.g.connect(self.n[0], self.n[i], both_ways=True)
        for i in range(1, 5):
            assert self.g.are_connected(self.n[0], self.n[i], both_ways=True)

    def test_connect_one_to_many_and_one_of_them_to_the_other(self):
        for i in range(1, 4):
            self.g.connect(self.n[0], self.n[i])
        self.g.connect(self.n[1], self.n[2])
        assert self.n[0].points_to(self.n[1])
        assert self.n[0].points_to(self.n[2])
        assert self.n[1].points_to(self.n[2])
        assert not self.n[2].points_to(self.n[1])

    def test_connect_many_to_one_single_direction(self):
        for i in range(1, 5):
            self.g.connect(self.n[i], self.n[0])
        for i in range(1, 5):
            assert self.n[i].points_to(self.n[0])
            assert not self.n[0].points_to(self.n[i])

    def test_connect_many_in_single_direction_with_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.connect(self.n[4], self.n[0])
        for i in range(4):
            assert self.n[i].points_to(self.n[i + 1])
        assert self.n[4].points_to(self.n[0])

    def test_connect_many_in_single_direction_without_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        for i in range(4):
            assert self.n[i].points_to(self.n[i + 1])
        assert not self.n[4].points_to(self.n[0])

    def test_connect_many_in_both_directions_with_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1], both_ways=True)
        self.g.connect(self.n[4], self.n[0], both_ways=True)
        for i in range(4):
            assert self.g.are_connected(
                self.n[i], self.n[i + 1], both_ways=True
            )
        assert self.g.are_connected(self.n[4], self.n[0], both_ways=True)

    def test_connect_many_in_both_directions_without_cycle(self):
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1], both_ways=True)
        for i in range(4):
            assert self.g.are_connected(
                self.n[i], self.n[i + 1], both_ways=True
            )
        assert not self.g.are_connected(self.n[4], self.n[0])
        assert not self.g.are_connected(self.n[0], self.n[4])

    def test_connect_many_to_many_in_both_directions(self):
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

    def test_disconnect_connected_nodes_in_single_direction(self):
        self.g.connect(self.n[0], self.n[1])
        assert self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[1], self.n[0])
        assert self.g.are_connected(self.n[0], self.n[1])
        self.g.disconnect(self.n[0], self.n[1])
        assert not self.g.are_connected(self.n[0], self.n[1])

    def test_disconnect_connected_nodes_in_both_directions(self):
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
