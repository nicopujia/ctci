import pytest

from src.stacks_and_queues import Stack


class TestStack:
    stack = Stack()

    def test_is_empty_on_new_stack(self):
        assert self.stack.is_empty()

    def test_peek_on_empty_stack_raises_index_error(self):
        with pytest.raises(IndexError):
            self.stack.peek()

    def test_pop_on_empty_stack_raises_index_error(self):
        with pytest.raises(IndexError):
            self.stack.pop()

    def test_push_and_peek_with_one_item(self):
        self.stack.push("a")
        assert not self.stack.is_empty()
        assert self.stack.peek() == "a"

    def test_push_and_peek_with_multiple_items(self):
        self.stack.push("a")
        assert self.stack.peek() == "a"
        self.stack.push("b")
        assert self.stack.peek() == "b"
        self.stack.push("c")
        assert self.stack.peek() == "c"

    def test_pop_removes_items_in_lifo_order(self):
        self.stack.push("a")
        self.stack.push("b")
        self.stack.push("c")
        self.stack.pop()
        assert self.stack.peek() == "b"
        self.stack.pop()
        assert self.stack.peek() == "a"
        self.stack.pop()
        assert self.stack.is_empty()
