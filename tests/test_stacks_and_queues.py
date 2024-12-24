import pytest

from src.stacks_and_queues import (
    AnimalShelter,
    Cat,
    Dog,
    MyQueue,
    Queue,
    SetOfStacks,
    SizedStack,
    Stack,
    StackMin,
    sort_stack,
)


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
        self.stack.push(1)
        assert not self.stack.is_empty()
        assert self.stack.peek() == 1

    def test_push_and_peek_with_multiple_items(self):
        self.stack.push(1)
        assert self.stack.peek() == 1
        self.stack.push(2)
        assert self.stack.peek() == 2
        self.stack.push(3)
        assert self.stack.peek() == 3

    def test_pop_items_in_lifo_order(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        assert self.stack.pop() == 3
        assert self.stack.pop() == 2
        assert self.stack.pop() == 1
        assert self.stack.is_empty()

    def test_repr_with_items(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        assert self.stack.__repr__() == "3 -> 2 -> 1"

    def test_repr_without_items(self):
        assert self.stack.__repr__() == "None"


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
        self.queue.add(1)
        assert not self.queue.is_empty()
        assert self.queue.peek() == 1

    def test_add_and_peek_with_multiple_items(self):
        self.queue.add(1)
        assert self.queue.peek() == 1
        self.queue.add(2)
        assert self.queue.peek() == 1
        self.queue.add(3)
        assert self.queue.peek() == 1

    def test_remove_items_in_fifo_order(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)
        assert self.queue.remove() == 1
        assert self.queue.remove() == 2
        assert self.queue.remove() == 3
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
        assert self.set_of_stacks.pop() == 3
        assert self.set_of_stacks.pop() == 2
        assert self.set_of_stacks.pop() == 1
        assert self.set_of_stacks.is_empty()

    def test_pop_exceding_threshold_once(self):
        items_count = int(SetOfStacks.threshold * 1.5)
        for i in range(items_count):
            self.set_of_stacks.push(i)
        for i in range(items_count, 0, -1):
            assert self.set_of_stacks.pop() == i - 1
        assert self.set_of_stacks.is_empty()

    def test_pop_without_items(self):
        with pytest.raises(IndexError):
            self.set_of_stacks.pop()


class TestMyQueue(TestQueue):
    def setup_method(self):
        self.queue = MyQueue()


class TestSortStack:
    def setup_method(self):
        self.stack = SizedStack()

    def test_sort_empty_stack(self):
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.is_empty()

    def test_sort_single_element_stack(self):
        self.stack.push(1)
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.peek() == 1

    def test_sort_already_sorted_stack(self):
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.pop() == 1
        assert sorted_stack.pop() == 2
        assert sorted_stack.pop() == 3
        assert sorted_stack.is_empty()

    def test_sort_reverse_sorted_stack(self):
        self.stack.push(3)
        self.stack.push(2)
        self.stack.push(1)
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.pop() == 1
        assert sorted_stack.pop() == 2
        assert sorted_stack.pop() == 3
        assert sorted_stack.is_empty()

    def test_sort_unsorted_stack(self):
        self.stack.push(3)
        self.stack.push(1)
        self.stack.push(2)
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.pop() == 1
        assert sorted_stack.pop() == 2
        assert sorted_stack.pop() == 3
        assert sorted_stack.is_empty()

    def test_sort_stack_with_duplicates(self):
        self.stack.push(2)
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(1)
        sorted_stack = sort_stack(self.stack)
        assert sorted_stack.pop() == 1
        assert sorted_stack.pop() == 1
        assert sorted_stack.pop() == 2
        assert sorted_stack.pop() == 2
        assert sorted_stack.is_empty()


class TestAnimalShelter:
    def setup_method(self):
        self.shelter = AnimalShelter()

    def test_dequeue_any_from_empty_shelter(self):
        with pytest.raises(IndexError):
            self.shelter.dequeue_any()

    def test_dequeue_dog_from_empty_shelter(self):
        with pytest.raises(IndexError):
            self.shelter.dequeue_dog()

    def test_dequeue_cat_from_empty_shelter(self):
        with pytest.raises(IndexError):
            self.shelter.dequeue_cat()

    def test_enqueue_and_dequeue_dogs(self):
        self.shelter.enqueue(Dog("Firulais"))
        self.shelter.enqueue(Dog("Rocky"))
        self.shelter.enqueue(Dog("Boxer"))
        assert self.shelter.dequeue_dog().name == "Firulais"
        assert self.shelter.dequeue_dog().name == "Rocky"
        assert self.shelter.dequeue_dog().name == "Boxer"

    def test_enqueue_and_dequeue_cats(self):
        self.shelter.enqueue(Cat("Maia"))
        self.shelter.enqueue(Cat("Mauricio"))
        self.shelter.enqueue(Cat("Enrique"))
        assert self.shelter.dequeue_cat().name == "Maia"
        assert self.shelter.dequeue_cat().name == "Mauricio"
        assert self.shelter.dequeue_cat().name == "Enrique"

    def test_enqueue_and_dequeue_any(self):
        self.shelter.enqueue(Dog("Firulais"))
        self.shelter.enqueue(Cat("Maia"))
        self.shelter.enqueue(Cat("Mauricio"))
        self.shelter.enqueue(Dog("Rocky"))
        self.shelter.enqueue(Dog("Boxer"))
        self.shelter.enqueue(Cat("Enrique"))
        assert self.shelter.dequeue_any().name == "Firulais"
        assert self.shelter.dequeue_any().name == "Maia"
        assert self.shelter.dequeue_any().name == "Mauricio"
        assert self.shelter.dequeue_any().name == "Rocky"
        assert self.shelter.dequeue_any().name == "Boxer"
        assert self.shelter.dequeue_any().name == "Enrique"

    def test_enqueue_cats_and_dequeue_dog(self):
        self.shelter.enqueue(Cat("Johnny"))
        self.shelter.enqueue(Cat("John"))
        with pytest.raises(IndexError):
            self.shelter.dequeue_dog()

    def test_enqueue_dogs_and_dequeue_cat(self):
        self.shelter.enqueue(Dog("George"))
        self.shelter.enqueue(Dog("Bob"))
        with pytest.raises(IndexError):
            self.shelter.dequeue_cat()

    def test_enqueue_all_and_dequeue_cat(self):
        self.shelter.enqueue(Dog("George"))
        self.shelter.enqueue(Cat("Johnny"))
        assert self.shelter.dequeue_cat().name == "Johnny"

    def test_enqueue_all_and_dequeue_dog(self):
        self.shelter.enqueue(Cat("Johnny"))
        self.shelter.enqueue(Dog("George"))
        assert self.shelter.dequeue_dog().name == "George"
