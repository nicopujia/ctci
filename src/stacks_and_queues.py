from typing import Any

from .linked_lists import LinkedListNode


class Stack:
    top: LinkedListNode | None = None

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack."""
        self.top = LinkedListNode(item, self.top if self.top else None)

    def pop(self) -> None:
        """Remove the top item from the stack."""
        if not self.top:
            raise IndexError
        self.top = self.top.next
        print(self.top)

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
