from typing import Any

from .linked_lists import LinkedListNode


class Stack:
    top: LinkedListNode | None = None

    def __repr__(self) -> str:
        return self.top.__repr__()

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack."""
        self.top = LinkedListNode(item, self.top if self.top else None)

    def pop(self) -> None:
        """Remove the top item from the stack."""
        if not self.top:
            raise IndexError
        self.top = self.top.next

    def peek(self) -> Any:
        """Return the top of the stack."""
        if not self.top:
            raise IndexError
        return self.top.data

    def is_empty(self) -> bool:
        """Return true if and only if the stack is empty."""
        return not bool(self.top)


class Queue:
    first: LinkedListNode | None = None
    last: LinkedListNode | None = None

    def add(self, item: Any) -> None:
        """Add an item to the end of the queue."""
        if self.last:
            self.last.next = LinkedListNode(item)
            self.last = self.last.next
        else:
            self.first = self.last = LinkedListNode(item)

    def remove(self) -> None:
        """Remove the first item in the queue."""
        if not self.first:
            raise IndexError
        self.first = self.first.next
        if not self.first:
            self.last = None

    def peek(self) -> Any:
        """Return the first of the queue."""
        if not self.first:
            raise IndexError
        return self.first.data

    def is_empty(self) -> bool:
        """Return true if and only if the queue is empty."""
        return not bool(self.first)


class StackMin(Stack):
    mins = Stack()

    def push(self, item: int) -> None:
        super().push(item)
        if self.mins.is_empty() or item < self.mins.peek():
            self.mins.push(item)

    def pop(self) -> None:
        if self.peek() == self.mins.peek():
            self.mins.pop()
        super().pop()

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
    stacks: list[SizedStack] = []

    def push(self, item: Any) -> None:
        if not self.stacks or self.stacks[-1].size >= self.threshold:
            self.stacks.append(SizedStack())
        self.stacks[-1].push(item)

    def pop(self, index: int = -1) -> None:
        if not self.stacks:
            raise IndexError
        self.stacks[index].pop()
        if not self.stacks[-1].size:
            self.stacks.pop()

    def peek(self) -> Any:
        return self.stacks[-1].peek()

    def is_empty(self) -> bool:
        return len(self.stacks) == 0


class MyQueue:
    def __init__(self):
        self.push_stack = Stack()
        self.pop_stack = Stack()

    def is_empty(self) -> bool:
        return self.push_stack.is_empty() and self.pop_stack.is_empty()

    def add(self, item: Any) -> None:
        self._reorganize(self.pop_stack, self.push_stack).push(item)

    def remove(self) -> None:
        self._reorganize(self.push_stack, self.pop_stack).pop()
        print(self.push_stack, self.pop_stack, sep="\n")

    def peek(self) -> Any:
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
