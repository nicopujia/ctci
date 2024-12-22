from dataclasses import dataclass
from typing import Type

from .linked_lists import Node as LinkedListNode


class Stack:
    top: LinkedListNode | None = None

    def __repr__(self) -> str:
        return self.top.__repr__()

    def push(self, item: int) -> None:
        self.top = LinkedListNode(item, self.top if self.top else None)

    def pop(self) -> int:
        if not self.top:
            raise IndexError
        old_item = self.top.data
        self.top = self.top.next
        return old_item

    def peek(self) -> int:
        if not self.top:
            raise IndexError
        return self.top.data

    def is_empty(self) -> bool:
        return not bool(self.top)


class Queue:
    first: LinkedListNode | None = None
    last: LinkedListNode | None = None

    def add(self, item: int) -> None:
        if self.last:
            self.last.next = LinkedListNode(item)
            self.last = self.last.next
        else:
            self.first = self.last = LinkedListNode(item)

    def remove(self) -> int:
        if not self.first:
            raise IndexError
        old_item = self.first.data
        self.first = self.first.next
        if not self.first:
            self.last = None
        return old_item

    def peek(self) -> int:
        if not self.first:
            raise IndexError
        return self.first.data

    def is_empty(self) -> bool:
        return not bool(self.first)


class StackMin(Stack):
    def __init__(self):
        super().__init__()
        self.mins = Stack()

    def push(self, item: int) -> None:
        super().push(item)
        if self.mins.is_empty() or item < self.mins.peek():
            self.mins.push(item)

    def pop(self) -> int:
        if self.peek() == self.mins.peek():
            self.mins.pop()
        return super().pop()

    def min(self) -> int:
        return self.mins.peek()


class SizedStack(Stack):
    size = 0

    def push(self, item):
        self.size += 1
        return super().push(item)

    def pop(self):
        self.size -= 1
        return super().pop()


class SetOfStacks:
    threshold = 5

    def __init__(self):
        self.stacks: list[SizedStack] = []

    def push(self, item: int) -> None:
        if not self.stacks or self.stacks[-1].size >= self.threshold:
            self.stacks.append(SizedStack())
        self.stacks[-1].push(item)

    def pop(self, index: int = -1) -> int:
        if not self.stacks:
            raise IndexError
        item = self.stacks[index].pop()
        if not self.stacks[-1].size:
            self.stacks.pop()
        return item

    def peek(self) -> int:
        return self.stacks[-1].peek()

    def is_empty(self) -> bool:
        return len(self.stacks) == 0


class MyQueue:
    def __init__(self):
        self.push_stack = Stack()
        self.pop_stack = Stack()

    def is_empty(self) -> bool:
        return self.push_stack.is_empty() and self.pop_stack.is_empty()

    def add(self, item: int) -> None:
        self._reorganize(self.pop_stack, self.push_stack).push(item)

    def remove(self) -> int:
        return self._reorganize(self.push_stack, self.pop_stack).pop()

    def peek(self) -> int:
        return self._reorganize(self.push_stack, self.pop_stack).peek()

    def _reorganize(self, src: Stack, dst: Stack) -> Stack:
        """Move all items from `src` to `dst`.

        Args:
            src (Stack): The stack containing the items.
            dst (Stack): The empty stack where items will be moved to.

        Returns:
            Stack:
                The originally empty stack now filled with all the items in
                reverse order.
        """
        while not src.is_empty():
            item = src.peek()
            src.pop()
            dst.push(item)
        return dst


def sort_stack(stack: SizedStack) -> SizedStack:
    if stack.size > 1:

        def move(src: Stack, dst: Stack) -> None:
            dst.push(src.pop())

        helper = Stack()
        move(stack, helper)

        while not stack.is_empty():
            if stack.peek() < helper.peek():
                # Swap top items
                stack_item = stack.pop()
                helper_item = helper.pop()
                stack.push(helper_item)
                helper.push(stack_item)

                if stack.size == 1:
                    move(helper, stack)
            else:
                move(stack, helper)

        while not helper.is_empty():
            move(helper, stack)

    return stack


@dataclass
class Animal:
    name: str


class Cat(Animal):
    pass


class Dog(Animal):
    pass


class AnimalShelter:
    def __init__(self):
        self.oldest: LinkedListNode | None = None
        self.newest: LinkedListNode | None = None

    def enqueue(self, animal: Animal) -> None:
        if self.newest:
            self.newest.next = LinkedListNode(animal)
            self.newest = self.newest.next
        else:
            self.oldest = self.newest = LinkedListNode(animal)

    def dequeue_any(self) -> Animal:
        if not self.oldest:
            raise IndexError
        oldest_animal = self.oldest.data
        self.oldest = self.oldest.next
        if not self.oldest:
            self.newest = None
        return oldest_animal

    def dequeue_dog(self) -> Dog:
        return self._dequeue_specific(Dog)

    def dequeue_cat(self) -> Cat:
        return self._dequeue_specific(Cat)

    def _dequeue_specific(self, animal_type: Type) -> Animal:
        if not self.oldest:
            raise IndexError

        if isinstance(self.oldest.data, animal_type):
            return self.dequeue_any()

        previous = self.oldest
        node = self.oldest.next
        while node and not isinstance(node.data, animal_type):
            previous = previous.next
            node = node.next

        if not node:
            raise IndexError()

        previous.next = node.next

        if node is self.newest:
            self.first = previous

        return node.data
