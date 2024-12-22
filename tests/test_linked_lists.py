import pytest

from src.linked_lists import (
    Node,
    delete_middle_node,
    get_kth_to_last,
    remove_dups,
)


class TestNode:
    def setup_method(self):
        self.head = Node(4, Node(2, Node(3, Node(1, Node(5)))))
        self.node = Node(1)

    def test_get_data(self):
        assert self.node.data == 1

    def test_set_data(self):
        self.node.data = 2
        assert self.node.data == 2

    def test_get_next(self):
        assert self.node.next is None

    def test_set_next(self):
        next_node = Node(2)
        self.node.next = next_node
        assert self.node.next is next_node

    def test_repr(self):
        assert self.node.__repr__() == "1"

    def test_linked_lists_next_and_data(self):
        assert self.head.data == 4
        assert self.head.next.data == 2
        assert self.head.next.next.data == 3
        assert self.head.next.next.next.data == 1
        assert self.head.next.next.next.next.data == 5
        assert self.head.next.next.next.next.next is None

    def test_linked_list_repr(self):
        assert self.head.__repr__() == "4 -> 2 -> 3 -> 1 -> 5"
        assert self.head.next.__repr__() == "2 -> 3 -> 1 -> 5"
        assert self.head.next.next.__repr__() == "3 -> 1 -> 5"
        assert self.head.next.next.next.__repr__() == "1 -> 5"
        assert self.head.next.next.next.next.__repr__() == "5"


class TestRemoveDups:
    def test_single_node(self):
        head = Node(1)
        assert remove_dups(head).__repr__() == "1"

    def test_no_dups(self):
        head = Node(1, Node(2, Node(3)))
        assert remove_dups(head).__repr__() == "1 -> 2 -> 3"

    def test_same_value_always(self):
        head = Node(1, Node(1, Node(1)))
        assert remove_dups(head).__repr__() == "1"

    def test_consecutive_dups(self):
        head = Node(1, Node(1, Node(2, Node(2))))
        assert remove_dups(head).__repr__() == "1 -> 2"

    def test_non_consecutive_dups(self):
        head = Node(1, Node(2, Node(1, Node(2))))
        assert remove_dups(head).__repr__() == "1 -> 2"

    def test_long_linked_list_with_dups(self):
        head = Node(1, Node(2, Node(3, Node(1, Node(1, Node(4, Node(3)))))))
        assert remove_dups(head).__repr__() == "1 -> 2 -> 3 -> 4"


class TestGetKthToLast:
    def setup_method(self):
        self.head = Node(44, Node(22, Node(33, Node(11, Node(55)))))
        self.node = Node(1)

    def test_with_k_below_length(self):
        assert get_kth_to_last(self.head, 2).data == 33

    def test_with_k_equals_zero(self):
        assert get_kth_to_last(self.head, 0).data == 55

    def test_with_k_equals_length(self):
        with pytest.raises(IndexError):
            get_kth_to_last(self.head, 5)

    def test_with_k_exceeding_length(self):
        with pytest.raises(IndexError):
            get_kth_to_last(self.head, 6)

    def test_single_node_with_k_equals_zero(self):
        assert get_kth_to_last(self.node, 0).data == 1

    def test_single_node_with_k_equals_length(self):
        with pytest.raises(IndexError):
            get_kth_to_last(self.node, 1)

    def test_single_node_with_k_exceding_length(self):
        with pytest.raises(IndexError):
            get_kth_to_last(self.node, 2)


class TestDeleteMiddleNode:
    def setup_method(self):
        self.head = Node(1, Node(2, Node(3)))

    def test_delete_first_node(self):
        delete_middle_node(self.head)
        assert self.head.__repr__() == "2 -> 3"

    def test_delete_second_node(self):
        delete_middle_node(self.head.next)
        assert self.head.__repr__() == "1 -> 3"

    def test_delete_last_node(self):
        delete_middle_node(self.head.next.next)
        assert self.head.__repr__() == "1 -> 2 -> 3"
