class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next
    
    def __repr__(self):
        return str(self.data) + (f" → {self.next}" if self.next else "")

    def __iter__(self):
        node = self
        yield node
        while node.next:
            node = node.next
            yield node

    def __next__(self):
        return self.next

    def __gt__(self, node):
        return self.data > node.data

    def __lt__(self, node):
        return self.data < node.data

    def insert_after(self, node):
        node.next = self.next
        self.next = node
    
    def append_to_tail(self, node):
        for tail in self:
            pass
        tail.next = node
    
    def remove_node(head, node):
        if head == node:
            return head

        prev = head
        while prev.next is not node and prev:
            prev = prev.next

        if prev:
            prev.next = prev.next.next
            return head

        raise ValueError()


class DoublyNode:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        return (
            f"{self.prev} <-> " if self.prev else ""
        ) + self.data + (
            f" <-> {self.next}" if self.next else ""
        )

    def insert_after(self, node):
        node.next = self.next
        node.prev = self
        self.next = node

    def append_to_tail(self, node):
        tail = self.get_tail()
        tail.next = node
        node.prev = tail
    
    def get_tail(self):
        tail = self
        while tail.next != None:
            tail = tail.next
        return tail
    
    def remove(self):
        self.next.prev = self.prev
        self.prev.next = self.next


def remove_dups(head): # O(n^2), O(1)
    # TODO: doesn't remove last element
    for node in head:
        if not node.next:
            break
        for following_node in node:
            if not following_node.next:
                break
            is_duplicate = node.data == following_node.next.data
            if is_duplicate:
                following_node.next = following_node.next.next
    return head


def get_kth_to_last(head, k): # O(n), O(1)
    length = 0
    for _ in head:
        length += 1
    
    for i, node in enumerate(head):
        if length - i == k:
            return node

    raise IndexError()

def delete_middle_node(node): # O(n), O(n)
    if self.next:
        self.data = self.next.data
        if self.next.next:
            self.next.delete()
        else:
            self.next = None
    else:
        self = None


def partition(head, x): 
    # Book solution:
    # O(n), O(1)
    tail = node = head
    while node:
        next = node.next
        if node < x:
            node.next = head
            head = node
        else:
            tail.next = node
            tail = node
        node = next
    tail.next = None
    return head

    # My solution:
    # O(n), O(n)
    left, right = [], []
    for node in head:
        if node < x:
            left.append(node)
        else:
            right.append(node)
    full = left + right
    for i in range(len(full)):
        full[i].next = full[i + 1] if i < len(full) - 1 else None
    return full[0]


def sum_lists(head_1, head_2): # O(n + m + d), O(d)
    def ll_to_int(head):
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


def sum_lists_follow_up(head_1, head_2): # O(n + m + d), O(d)
    def ll_to_int(head):
        length = 0
        for _ in head:
            length += 1
        
        num = 0
        for i, node in enumerate(head, 1):
            num += node.data * 10**(length - i)

        return num
    
    num = str(ll_to_int(head_1) + ll_to_int(head_2))
    
    head = tail = Node(int(num[0]))
    for digit in num[1:]:
        tail.next = Node(int(digit))
        tail = tail.next
        
    return head


def check_palindrome(head): # O(n), O(1)
    length = 0
    for _ in head:
        length += 1
    
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
  

def check_intersection(head_1, head_2): # O(n), O(1)
    for n, m in zip(head_1, head_2):
        if n is m:
            return True
    return False


def detect_loop(head): # O(n^2), O(1)
    for node in head:
        for checking_node in head:
            if checking_node is node.next:
                # returning .data to avoid recrusion error provocated by the
                # __repr__ method
                return checking_node.data
            
            if checking_node is node:
                break            
