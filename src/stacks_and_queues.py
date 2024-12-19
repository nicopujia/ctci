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
