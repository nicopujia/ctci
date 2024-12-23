from src.trees_and_graphs import Node


class TestNode:
    def setup_method(self):
        self.n = [Node(i) for i in range(5)]

    def test_nodes_data(self):
        for i in range(len(self.n)):
            assert self.n[i].data == i

    def test_no_neighbors_initially(self):
        for i in range(5):
            assert len(self.n[i].neighbors) == 0

    def test_connect_one_to_itself(self):
        self.n[0].connect(self.n[0])
        assert self.n[0].is_connected(self.n[0])

    def test_connect_one_to_another_in_single_direction(self):
        self.n[0].connect(self.n[1])
        assert self.n[0].is_connected(self.n[1])
        assert not self.n[1].is_connected(self.n[1])

    def test_connect_same_nodes_multiple_times_keeps_one_connection(self):
        self.n[0].connect(self.n[1])
        self.n[0].connect(self.n[1])
        assert len(self.n[0].neighbors) == 1

    def test_connect_one_to_another_in_both_directions(self):
        self.n[0].connect(self.n[1])
        self.n[1].connect(self.n[0])
        assert self.n[0].is_connected(self.n[1])
        assert self.n[1].is_connected(self.n[0])

    def test_connect_one_to_many_single_direction(self):
        for i in range(1, 5):
            self.n[0].connect(self.n[i])
        for i in range(1, 5):
            assert self.n[0].is_connected(self.n[i])
            assert not self.n[i].is_connected(self.n[0])

    def test_connect_one_to_many_in_both_directions(self):
        for i in range(1, 5):
            self.n[0].connect(self.n[i])
            self.n[i].connect(self.n[0])
        for i in range(1, 5):
            assert self.n[0].is_connected(self.n[i])
            assert self.n[i].is_connected(self.n[0])

    def test_connect_one_to_many_and_one_of_them_to_the_other(self):
        for i in range(1, 4):
            self.n[0].connect(self.n[i])
        self.n[1].connect(self.n[2])
        assert self.n[0].is_connected(self.n[1])
        assert self.n[0].is_connected(self.n[2])
        assert self.n[1].is_connected(self.n[2])
        assert not self.n[2].is_connected(self.n[1])

    def test_connect_many_to_one_single_direction(self):
        for i in range(1, 5):
            self.n[i].connect(self.n[0])
        for i in range(1, 5):
            assert self.n[i].is_connected(self.n[0])
            assert not self.n[0].is_connected(self.n[i])

    def test_connect_many_in_single_direction_with_cycle(self):
        for i in range(4):
            self.n[i].connect(self.n[i + 1])
        self.n[4].connect(self.n[0])
        for i in range(4):
            assert self.n[i].is_connected(self.n[i + 1])
        assert self.n[4].is_connected(self.n[0])

    def test_connect_many_in_single_direction_without_cycle(self):
        for i in range(4):
            self.n[i].connect(self.n[i + 1])
        for i in range(4):
            assert self.n[i].is_connected(self.n[i + 1])
        assert not self.n[4].is_connected(self.n[0])

    def test_connect_many_in_both_directions_with_cycle(self):
        for i in range(4):
            self.n[i].connect(self.n[i + 1])
            self.n[i + 1].connect(self.n[i])
        self.n[4].connect(self.n[0])
        self.n[0].connect(self.n[4])
        for i in range(4):
            assert self.n[i].is_connected(self.n[i + 1])
            assert self.n[i + 1].is_connected(self.n[i])
        assert self.n[4].is_connected(self.n[0])
        assert self.n[0].is_connected(self.n[4])

    def test_connect_many_in_both_directions_without_cycle(self):
        for i in range(4):
            self.n[i].connect(self.n[i + 1])
            self.n[i + 1].connect(self.n[i])
        for i in range(4):
            assert self.n[i].is_connected(self.n[i + 1])
            assert self.n[i + 1].is_connected(self.n[i])
        assert not self.n[4].is_connected(self.n[0])
        assert not self.n[0].is_connected(self.n[4])

    def test_connect_many_to_many_in_both_directions(self):
        for i in range(5):
            for j in range(5):
                if j == i:
                    continue
                self.n[i].connect(self.n[j])
        for i in range(5):
            for j in range(5):
                if j == i:
                    assert not self.n[i].is_connected(self.n[j])
                else:
                    assert self.n[i].is_connected(self.n[j])

    def test_disconnect_disconnected_nodes_does_nothing(self):
        assert not self.n[0].is_connected(self.n[1])
        self.n[0].disconnect(self.n[1])
        assert not self.n[0].is_connected(self.n[1])

    def test_disconnect_connected_nodes_in_single_direction(self):
        self.n[0].connect(self.n[1])
        assert self.n[0].is_connected(self.n[1])
        assert not self.n[1].is_connected(self.n[0])
        self.n[1].disconnect(self.n[0])
        assert self.n[0].is_connected(self.n[1])
        assert not self.n[1].is_connected(self.n[0])
        self.n[0].disconnect(self.n[1])
        assert not self.n[0].is_connected(self.n[1])
        assert not self.n[1].is_connected(self.n[0])

    def test_disconnect_connected_nodes_in_both_direction(self):
        self.n[0].connect(self.n[1])
        self.n[1].connect(self.n[0])
        assert self.n[0].is_connected(self.n[1])
        assert self.n[1].is_connected(self.n[0])
        self.n[0].disconnect(self.n[1])
        assert not self.n[0].is_connected(self.n[1])
        assert self.n[1].is_connected(self.n[0])
        self.n[1].disconnect(self.n[0])
        assert not self.n[0].is_connected(self.n[1])
        assert not self.n[1].is_connected(self.n[0])
