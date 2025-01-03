from src.trees_and_graphs import (
    Graph,
    Node,
    TreeNode,
    UndirectedGraph,
    UndirectedNode,
    check_balanced,
    check_route,
    generate_minimal_bst,
    get_lists_of_depths,
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

    def test_connect_outside_to_inside_node_in_one_way(self):
        node = Node(10)
        self.g.connect(node, self.n[0])
        assert node.points_to(self.n[0])
        assert not self.n[0].points_to(node)
        assert node in self.g.nodes
        assert self.n[0] in self.g.nodes

    def test_connect_outside_to_inside_node_in_the_other_way(self):
        node = Node(10)
        self.g.connect(self.n[0], node)
        assert self.g.are_connected(node, self.n[0])
        assert node in self.g.nodes
        assert self.n[0] in self.g.nodes

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
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.remove(self.n[1])
        assert self.n[0] in self.g.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[2] in self.g.nodes
        assert self.n[3] in self.g.nodes
        assert self.g.are_connected(self.n[2], self.n[3])
        for i in range(4):
            assert self.n[1] not in self.n[i].neighbors

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

    def test_connect_outside_to_inside_node(self):
        node = UndirectedNode(10)
        self.g.connect(node, self.n[0])
        assert self.g.are_connected(node, self.n[0])
        assert node in self.g.nodes
        assert self.n[0] in self.g.nodes

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
        for i in range(4):
            self.g.connect(self.n[i], self.n[i + 1])
        self.g.remove(self.n[1])
        assert self.n[0] in self.g.nodes
        assert self.n[1] not in self.g.nodes
        assert self.n[2] in self.g.nodes
        assert self.n[3] in self.g.nodes
        assert self.g.are_connected(self.n[2], self.n[3])
        for i in range(4):
            assert self.n[1] not in self.n[i].neighbors

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


class TestTreeNode:
    def setup_method(self):
        self.root = TreeNode(0)

    def test_root_node(self):
        assert self.root.data == 0
        assert self.root.parent is None
        assert not self.root.children

    def test_init_one_child(self):
        child = TreeNode(1, parent=self.root)
        assert child in self.root.children
        assert child.parent is self.root
        assert not child.children

    def test_init_multiple_children(self):
        for i in range(1, 11):
            child = TreeNode(i, parent=self.root)
            assert child in self.root.children
            assert child.parent == self.root
            assert not child.children
        assert len(self.root.children) == 10

    def test_init_grandchild(self):
        child = TreeNode(1, parent=self.root)
        grandchild = TreeNode(2, parent=child)
        assert len(self.root.children) == 1
        assert grandchild in child.children
        assert grandchild.parent is child
        assert not grandchild.children

    def test_add_child(self):
        future_child = TreeNode(1)
        assert future_child.parent is None
        assert future_child not in self.root.children
        self.root.add_child(future_child)
        assert future_child in self.root.children
        assert future_child.parent is self.root

    def test_remove_child(self):
        child = TreeNode(1, parent=self.root)
        self.root.remove_child(child)
        assert child not in self.root.children
        assert child.parent is None

    def test_repr(self):
        child = TreeNode(1, parent=self.root)
        grandchild = TreeNode(2, parent=child)
        assert repr(self.root) == "TreeNode(0)"
        assert repr(child) == "TreeNode(1, parent=TreeNode(0))"
        assert (
            repr(grandchild)
            == "TreeNode(2, parent=TreeNode(1, parent=TreeNode(0)))"
        )


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


class TestGenerateMinimalBST:
    def assert_node(
        self,
        node: TreeNode,
        expected_data,
        expected_parent: TreeNode | None,
        expected_children_count: int,
    ):
        assert node.data == expected_data
        assert node.parent is expected_parent
        assert len(node.children) == expected_children_count

    def test_one_element(self):
        root = generate_minimal_bst([1])
        self.assert_node(root, 1, None, 0)

    def test_two_elements(self):
        root = generate_minimal_bst(range(1, 3))
        self.assert_node(root, 2, None, 1)
        self.assert_node(root.children[0], 1, root, 0)

    def test_three_elements(self):
        root = generate_minimal_bst(range(1, 4))
        self.assert_node(root, 2, None, 2)
        self.assert_node(root.children[0], 1, root, 0)
        self.assert_node(root.children[1], 3, root, 0)

    def test_large_even_amount_of_elements(self):
        root = generate_minimal_bst(range(1, 11))
        self.assert_node(root, 6, None, 2)
        l, r = root.children
        self.assert_node(l, 3, root, 2)
        self.assert_node(r, 9, root, 2)
        self.assert_node(l.children[0], 2, l, 1)
        self.assert_node(l.children[1], 5, l, 1)
        self.assert_node(r.children[0], 8, r, 1)
        self.assert_node(r.children[1], 10, r, 0)
        self.assert_node(l.children[0].children[0], 1, l.children[0], 0)
        self.assert_node(l.children[1].children[0], 4, l.children[1], 0)
        self.assert_node(r.children[0].children[0], 7, r.children[0], 0)

    def test_large_odd_amount_of_elements(self):
        root = generate_minimal_bst(range(1, 12))
        self.assert_node(root, 6, None, 2)
        l, r = root.children
        self.assert_node(l, 3, root, 2)
        self.assert_node(r, 9, root, 2)
        self.assert_node(l.children[0], 2, l, 1)
        self.assert_node(l.children[1], 5, l, 1)
        self.assert_node(r.children[0], 8, r, 1)
        self.assert_node(r.children[1], 11, r, 1)
        self.assert_node(l.children[0].children[0], 1, l.children[0], 0)
        self.assert_node(l.children[1].children[0], 4, l.children[1], 0)
        self.assert_node(r.children[0].children[0], 7, r.children[0], 0)
        self.assert_node(r.children[1].children[0], 10, r.children[1], 0)


class TestGetListsOfDepth:
    def test_with_one_level(self):
        root = generate_minimal_bst([1])
        lists = get_lists_of_depths(root)
        assert len(lists) == 1
        assert str(lists[0]) == "1"

    def test_with_two_levels(self):
        root = generate_minimal_bst(range(1, 4))
        lists = get_lists_of_depths(root)
        assert len(lists) == 2
        assert str(lists[0]) == "2"
        assert str(lists[1]) == "1 -> 3"

    def test_with_three_levels(self):
        root = generate_minimal_bst(range(1, 7))
        lists = get_lists_of_depths(root)
        assert len(lists) == 3
        assert str(lists[0]) == "4"
        assert str(lists[1]) == "2 -> 6"
        assert str(lists[2]) == "1 -> 3 -> 5"


class TestCheckBalanced:
    def setup_method(self):
        self.root = TreeNode(1)

    def test_one_node(self):
        assert check_balanced(self.root)

    def test_two_nodes(self):
        self.root.add_child(TreeNode(2))
        assert check_balanced(self.root)

    def test_three_nodes_balanced(self):
        self.root.add_child(TreeNode(2))
        self.root.add_child(TreeNode(3))
        assert check_balanced(self.root)

    def test_three_nodes_unbalanced(self):
        child = TreeNode(2, parent=self.root)
        child.add_child(TreeNode(3))
        assert not check_balanced(self.root)

    def test_ten_nodes_balanced(self):
        assert check_balanced(generate_minimal_bst(range(10)))

    def test_ten_nodes_unbalanced(self):
        root = generate_minimal_bst(range(10))
        leaf = root.children[0].children[1].children[0]
        leaf.parent.remove_child(leaf)
        root.children[0].children[0].children[0].add_child(leaf)
        assert not check_balanced(self.root)
