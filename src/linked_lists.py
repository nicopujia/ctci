from dataclasses import dataclass
from typing import Iterator, Self


@dataclass
class Node:
    data: int
    next: Self | None = None

    def __repr__(self) -> str:
        return str(self.data) + (f" -> {self.next}" if self.next else "")

    def __iter__(self) -> Iterator[Self]:
        node = self
        yield node
        while node.next:
            node = node.next
            yield node

    def get_length(self):
        length = 0
        for _ in self:
            length += 1
        return length


# O(n^2), O(1)
def remove_dups(head: Node) -> Node:
    for node in head:
        if not node.next:
            break
        following_node_previous = node
        for following_node in node.next:
            if following_node.data == node.data:
                following_node_previous.next = following_node.next
            else:
                following_node_previous = following_node_previous.next
    return head


# O(n), O(1)
def get_kth_to_last(head: Node, k: int) -> Node:
    length = head.get_length()

    for i, node in enumerate(head, 1):
        if length - i == k:
            return node

    raise IndexError()


# O(n), O(n)
def delete_middle_node(node: Node) -> None:
    if node.next:
        node.data = node.next.data
        if node.next.next:
            node.next = node.next.next
        else:
            node.next = None
    else:
        node = None


# O(n), O(n)*
def partition(head: Node, x: int) -> Node:
    left, right = [], []
    for node in head:
        if node.data < x:
            left.append(node)
        else:
            right.append(node)
    full = left + right
    for i in range(len(full)):
        full[i].next = full[i + 1] if i < len(full) - 1 else None
    return full[0]


# O(n + m + d), O(d)
def sum_lists(head_1: Node, head_2: Node) -> Node:
    def ll_to_int(head: Node) -> int:
        num = 0
        for i, node in enumerate(head):
            num += node.data * 10**i
        return num

    num = ll_to_int(head_1) + ll_to_int(head_2)
    head = tail = Node(num % 10)

    while num // 10 > 0:
        num //= 10
        tail.next = Node(num % 10)
        tail = tail.next

    return head


# O(n + m + d), O(d)
def sum_lists_follow_up(head_1: Node, head_2: Node) -> Node:
    def ll_to_int(head: Node):
        length = head.get_length()

        num = 0
        for i, node in enumerate(head, 1):
            num += node.data * 10 ** (length - i)

        return num

    num = str(ll_to_int(head_1) + ll_to_int(head_2))

    head = tail = Node(int(num[0]))
    for digit in num[1:]:
        tail.next = Node(int(digit))
        tail = tail.next

    return head


# O(n), O(1)
def check_palindrome(head: Node) -> bool:
    length = head.get_length()

    if length == 1:
        return True

    node = head.next
    head.next = None
    i = 1
    while i < length // 2:
        i += 1
        old_next = node.next
        node.next = head
        head = node
        node = old_next

    for n, m in zip(head, node if length % 2 == 0 else node.next):
        if n.data != m.data:
            return False
    return True


# O(n), O(1)
def check_intersection(head_1: Node, head_2: Node) -> bool:
    length_1 = head_1.get_length()
    length_2 = head_2.get_length()
    longer_head = head_1 if length_1 > length_2 else head_2
    longer_length = length_1 if length_1 > length_2 else length_2
    shorter_length = length_1 if length_1 <= length_2 else length_2
    length_difference = longer_length - shorter_length

    while length_difference:
        length_difference -= 1
        longer_head.next = longer_head.next.next

    for n, m in zip(head_1, head_2):
        if n.next is m.next and n.next is not None:
            return True

    return False


# O(n^2), O(1)
def detect_loop(head: Node) -> Node:
    for node in head:
        for checking_node in head:
            if checking_node is node.next:
                return checking_node

            if checking_node is node:
                break
