from typing import Any, Iterable, Self


class Node:
    def __init__(self, data: Any):
        self.data = data
        self.neighbors = set()

    def __repr__(self) -> str:
        return f"{self.data} -> " + ", ".join(
            neighbor.data for neighbor in self.neighbors
        )

    def connect(self, other: Self) -> None:
        self.neighbors.add(other)

    def disconnect(self, other: Self) -> None:
        self.neighbors.discard(other)

    def is_connected(self, other: Self) -> bool:
        return other in self.neighbors
