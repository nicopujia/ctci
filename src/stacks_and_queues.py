from typing import Any

from .linked_lists import Node


class Stack:
    head = None

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack."""
        self.head = Node(item, self.head if self.head else None)

    def pop(self) -> None:
        """Remove the top item from the stack."""
        if not self.head:
            raise IndexError
        self.head = self.head.next
        print(self.head)

    def peek(self) -> Any:
        """Return the top of the stack."""
        if not self.head:
            raise IndexError
        return self.head.data

    def is_empty(self) -> bool:
        """Return true if and only if the stack is empty."""
        return not bool(self.head)
