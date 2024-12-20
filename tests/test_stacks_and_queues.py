import pytest

from src.stacks_and_queues import Queue, Stack


class TestStack:
    def setup_method(self):
        self.stack = Stack()

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

    def test_pop_items_in_lifo_order(self):
        self.stack.push("a")
        self.stack.push("b")
        self.stack.push("c")
        self.stack.pop()
        assert self.stack.peek() == "b"
        self.stack.pop()
        assert self.stack.peek() == "a"
        self.stack.pop()
        assert self.stack.is_empty()


class TestQueue:
    def setup_method(self):
        self.queue = Queue()

    def test_is_empty_on_new_queue(self):
        assert self.queue.is_empty()

    def test_peek_on_empty_queue_raises_index_error(self):
        with pytest.raises(IndexError):
            self.queue.peek()

    def test_remove_on_empty_queue_raises_index_error(self):
        with pytest.raises(IndexError):
            self.queue.remove()

    def test_add_and_peek_with_one_item(self):
        self.queue.add("a")
        assert not self.queue.is_empty()
        assert self.queue.peek() == "a"

    def test_add_and_peek_with_multiple_items(self):
        self.queue.add("a")
        assert self.queue.peek() == "a"
        self.queue.add("b")
        assert self.queue.peek() == "a"
        self.queue.add("c")
        assert self.queue.peek() == "a"

    def test_remove_items_in_fifo_order(self):
        self.queue.add("a")
        self.queue.add("b")
        self.queue.add("c")
        self.queue.remove()
        assert self.queue.peek() == "b"
        self.queue.remove()
        assert self.queue.peek() == "c"
        self.queue.remove()
        assert self.queue.is_empty()
