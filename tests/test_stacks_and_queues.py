import pytest

from src.stacks_and_queues import Queue, SetOfStacks, Stack, StackMin


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


class TestStackMin(TestStack):
    def setup_method(self):
        self.stack = StackMin()

    def test_min_after_pushes_and_pops(self):
        self.stack.push(5)
        self.stack.push(7)
        self.stack.pop()
        self.stack.push(4)
        self.stack.push(1)
        self.stack.pop()
        self.stack.push(2)
        self.stack.push(3)
        self.stack.pop()
        self.stack.push(6)
        self.stack.push(8)
        self.stack.pop()
        assert self.stack.min() == 2


class TestSetOfStacks:
    def setup_method(self):
        self.set_of_stacks = SetOfStacks()
        self.set_of_stacks.stacks = []

    def test_is_empty_on_empty_set(self):
        assert self.set_of_stacks.is_empty()

    def test_push_and_peek_below_threshold(self):
        self.set_of_stacks.push(1)
        assert self.set_of_stacks.peek() == 1
        self.set_of_stacks.push(2)
        assert self.set_of_stacks.peek() == 2
        self.set_of_stacks.push(3)
        assert self.set_of_stacks.peek() == 3

    def test_push_and_peek_exceding_threshold_once(self):
        for i in range(int(SetOfStacks.threshold * 1.5)):
            self.set_of_stacks.push(i)
            assert self.set_of_stacks.peek() == i

    def test_push_and_peek_exceding_threshold_many_times(self):
        for i in range(SetOfStacks.threshold * 10):
            self.set_of_stacks.push(i)
            assert self.set_of_stacks.peek() == i

    def test_pop_below_threshold(self):
        self.set_of_stacks.push(1)
        self.set_of_stacks.push(2)
        self.set_of_stacks.push(3)
        self.set_of_stacks.pop()
        assert self.set_of_stacks.peek() == 2
        self.set_of_stacks.pop()
        assert self.set_of_stacks.peek() == 1
        self.set_of_stacks.pop()
        assert self.set_of_stacks.is_empty()

    def test_pop_exceding_threshold_once(self):
        items_count = int(SetOfStacks.threshold * 1.5)
        for i in range(items_count):
            self.set_of_stacks.push(i)
        for i in range(items_count, 0, -1):
            self.set_of_stacks.pop()
            if i > 1:
                assert self.set_of_stacks.peek() == i - 2
        assert self.set_of_stacks.is_empty()
