# ENGINEERING VERIFICATION AND VALIDATION SIGN-OFF
# Engineer Name: Tala Abusalah
#
# By signing my name above, I confirm that I have reviewed this
# implementation as a software engineer would before approving work
# for release. I verified it against the stated requirements, validated
# its behavior with tests, and evaluated whether it preserves the
# required data-structure invariants.
#
# Based on the evidence I collected, I am willing to attach my name
# to this solution and sign off on its submission. I accept professional
# responsibility for the complete solution, including any portions
# developed with generative AI assistance.

"""
CSE 331
Project 1
"""

from __future__ import annotations

from typing import List, TypeVar

T = TypeVar("T")
Node = TypeVar("Node")


class Node:
    """
    Implementation of a doubly linked list node.
    DO NOT MODIFY
    """
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T, next: Node = None, prev: Node = None) -> None:
        """
        Construct a doubly linked list node.

        :param value: value held by the Node.
        :param next: reference to the next Node in the linked list.
        :param prev: reference to the previous Node in the linked list.
        :return: None.
        DO NOT MODIFY
        """
        self.next = next
        self.prev = prev
        self.value = value

    def __repr__(self) -> str:
        """
        Represents the Node as a string.

        :return: string representation of the Node.
        DO NOT MODIFY
        """
        return f"Node({str(self.value)})"

    __str__ = __repr__


class DLL:
    """
    Implementation of a doubly linked list without sentinel (padding) nodes.
    Modify only below the indicated line.
    """
    __slots__ = ["head", "tail", "size"]

    def __init__(self) -> None:
        """
        Construct an empty doubly linked list.

        :return: None.
        DO NOT MODIFY
        """
        self.head = self.tail = None
        self.size = 0

    def __repr__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        DO NOT MODIFY
        """
        result = []
        node = self.head
        while node is not None:
            result.append(str(node))
            node = node.next
        return " <-> ".join(result)

    def __str__(self) -> str:
        """
        Represent the DLL as a string.

        :return: string representation of the DLL.
        DO NOT MODIFY
        """
        return repr(self)

    # MODIFY BELOW #

    def empty(self) -> bool:
        """
        Returns whether the DLL is empty.
        """
        return self.size == 0

    def push(self, val: T, back: bool = True) -> None:
        """
        Adds a new node containing val to the front or back of the DLL.
        """
        new_node = Node(val)
        if self.empty():
            self.head = new_node
            self.tail = new_node
        elif back:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def pop(self, back: bool = True) -> None:
        """
        Removes a node from the front or back of the DLL.
        """
        if self.empty():
            return

        if self.size == 1:
            self.head = None
            self.tail = None
            self.size = 0
            return

        if back:
            self.tail = self.tail.prev
            self.tail.next = None
        else:
            self.head = self.head.next
            self.head.prev = None

        self.size -= 1

    def list_to_dll(self, source: List[T]) -> None:
        """
        Replaces the current DLL with nodes containing the values from source.
        """
        self.head = None
        self.tail = None
        self.size = 0

        for value in source:
            self.push(value)

    def dll_to_list(self) -> List[T]:
        """
        Returns a list containing the values of the DLL in order.
        """
        result = []
        current = self.head

        while current is not None:
            result.append(current.value)
            current = current.next

        return result

    def _find_nodes(self, val: T, find_first: bool = False) -> List[Node]:
        """
        Finds nodes containing val, optionally stopping after the first match.
        """
        found = []
        current = self.head
        while current is not None:
            if current.value == val:
                found.append(current)

                if find_first:
                    break

            current = current.next

        return found

    def find(self, val: T) -> Node:
        """
        Returns the first node containing val, or None if no match is found.
        """
        nodes = self._find_nodes(val, find_first=True)

        if nodes:
            return nodes[0]

        return None

    def find_all(self, val: T) -> List[Node]:
        """
        Returns a list of all nodes containing val.
        """
        return self._find_nodes(val)

    def remove_node(self, to_remove: Node) -> None:
        """
        Removes the specified node from the DLL.
        """
        if to_remove == self.head:
            self.pop(back=False)
            return

        if to_remove == self.tail:
            self.pop(back=True)
            return

        to_remove.prev.next = to_remove.next
        to_remove.next.prev = to_remove.prev
        self.size -= 1

    def remove(self, val: T) -> bool:
        """
        Removes the first node containing val and returns whether a node was removed.
        """
        node = self.find(val)

        if node is None:
            return False

        self.remove_node(node)
        return True

    def remove_all(self, val: T) -> int:
        """
        Removes all nodes containing val and returns the number of nodes removed.
        """
        nodes = self.find_all(val)

        for node in nodes:
            self.remove_node(node)

        return len(nodes)

    def reverse(self) -> None:
        """
        Reverses the order of the nodes in the DLL.
        """
        current = self.head
        while current is not None:
            current.prev, current.next = current.next, current.prev
            current = current.prev

        self.head, self.tail = self.tail, self.head


class BrowserHistory:
    """
    Browser back/forward navigation backed by a DLL (classic interview design).
    """

    def __init__(self, homepage: str) -> None:
        """
        Initializes the browser history with the given homepage as the current page.
        """
        self.history = DLL()
        self.history.push(homepage)
        self.current = self.history.head

    def visit(self, url: str) -> None:
        """
        Visits a new URL and clears any forward browsing history.
        """
        while self.current.next is not None:
            self.history.remove_node(self.current.next)

        self.history.push(url)
        self.current = self.history.tail

    def back(self, steps: int) -> str:
        """
        Moves backward in the browser history by up to the given number of steps.
        """
        while steps > 0 and self.current.prev is not None:
            self.current = self.current.prev
            steps -= 1

        return self.current.value

    def forward(self, steps: int) -> str:
        """
        Moves forward in the browser history by up to the given number of steps.
        """
        while steps > 0 and self.current.next is not None:
            self.current = self.current.next
            steps -= 1

        return self.current.value
