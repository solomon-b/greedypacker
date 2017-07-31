#!/usr/bin/env python
""" Class based AVL balanced binary search tree.
A tree constists of a single AVL_Tree object and
many Node objects.

What distinguises AVL_Tree from a plain Binary Search Tree is
it's self balancing property. Whenever a node is inserted or
deleted, the balance factors of the affected nodes are checked
and Nodes are rotated to maintain balance in the tree. This
ensures O(logN) insertion, deletion, and search performance.
"""
from typing import Optional

class Node(object):
    #__slots__ = ('key', 'left', 'right', 'parent', 'height', 'count')
    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.height = 1
        self.count = 1
        self.data = []


class AvlTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, current_node: Node) -> None:
        """ Performs a right rotation for balancing the tree """
        left_child = current_node.left
        current_node.left = left_child.right
        if left_child.right != None:
            left_child.right.parent = current_node
        left_child.parent = current_node.parent
        if self.root == current_node:
            self.root = left_child
        else:
            if current_node.parent.left == current_node:
                current_node.parent.left = left_child
            else:
                current_node.parent.right = left_child
        left_child.right = current_node
        current_node.parent = left_child

        current_node.height = max(
            current_node.left.height if current_node.left else 0,
            current_node.right.height if current_node.right else 0) + 1
        left_child.height = max(
            left_child.left.height if left_child.left else 0,
            left_child.right.height if left_child.right else 0) + 1

    def left_rotate(self, current_node: Node) -> None:
        """ Performs a left rotation for balancing the tree """
        right_child = current_node.right
        current_node.right = right_child.left

        if right_child.left != None:
            right_child.left.parent = current_node
        right_child.parent = current_node.parent

        if self.root == current_node:
            self.root = right_child
        else:
            if current_node.parent.left == current_node:
                current_node.parent.left = right_child
            else:
                current_node.parent.right = right_child
        right_child.left = current_node
        current_node.parent = right_child

        current_node.height = max(
            current_node.left.height if current_node.left else 0,
            current_node.right.height if current_node.right else 0) + 1
        right_child.height = max(
            right_child.left.height if right_child.left else 0,
            right_child.right.height if right_child.right else 0) + 1

    @staticmethod
    def get_balance(node: Node) -> int:
        """ Returns balance factor for a node """
        if node is None:
            return 0
        return (node.left.height if node.left else 0) - (node.right.height if node.right else 0)

    def rotate_manager(self, node: Node, inserted_key: int, balance: int) -> None:

        if balance > 1 and inserted_key < node.left.key:
            # Left Left
            self.right_rotate(node)
        elif balance < -1 and inserted_key > node.right.key:
            # Right Right
            self.left_rotate(node)
        elif balance > 1 and inserted_key > node.left.key:
            # Left Right
            self.left_rotate(node.left)
            self.right_rotate(node)
        elif balance < -1 and inserted_key < node.right.key:
            # Right Left
            self.right_rotate(node.right)
            self.left_rotate(node)

    def insert(self, key: int, insertion_point=None) -> Node:
        """ Insert new node into the tree """
        node = Node(key)
        # If the tree is empty then assign new node to root
        if self.root is None:
            self.root = node
            return node

        if insertion_point is None:
            insertion_point = self.root

        search_queue = [insertion_point]
        index = 0
        while search_queue:
            if key == search_queue[index].key:
                search_queue[index].count += 1
                return search_queue[index]
            elif key < search_queue[index].key:
                if search_queue[index].left:
                    search_queue.append(search_queue[index].left)
                    index += 1
                else:
                    search_queue[index].left = node
                    node.parent = search_queue[index]
                    break
            elif key > search_queue[index].key:
                if search_queue[index].right:
                    search_queue.append(search_queue[index].right)
                    index += 1
                else:
                    search_queue[index].right = node
                    node.parent = search_queue[index]
                    break

        for queued_node in reversed(search_queue):
            queued_node.height = max(
                queued_node.left.height if queued_node.left else 0,
                queued_node.right.height if queued_node.right else 0) + 1
            balance = self.get_balance(queued_node)
            if balance > 1 or balance < -1:
                self.rotate_manager(queued_node, key, balance)
        return node


    def get(self, key: int) -> Optional[Node]:
        """ Returns a node with key if found in tree """
        if self.root:
            node = self._get(key, self.root)
            if node:
                return node
            return None
        return None

    def _get(self, key: int, current_node: Node) -> Optional[Node]:
        """ Recursive search method called by get() """
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left)
        return self._get(key, current_node.right)

    def __getitem__(self, key: int):
        """ Overloads [] getter to use get() """
        return self.get(key)

    def __contains__(self, key):
        return bool(self.get(key))

    def min_value(self, key: int) -> int:
        """ Return the lowest value key in subtree with root 'node' """
        sub_tree_root = self.get(key)
        while sub_tree_root.left != None:
            sub_tree_root = sub_tree_root.left
        return sub_tree_root.key

    def delete(self, key: int, starting_node: Node = None) -> None:
        """
        When removing a node there are three cases:
            1. The node has no children:
                Delete pointer in parent node and
                delete node object.
            2. The node has one child:
                Promote the child to take node's place
                then delete node object.
            3. The node has two children:
                Search tree for a node that can replace
                the node and preserve the binary structure
                This will be the next largest node in
                the tree and will never have two children.
                This means it can be removed and swapped
                in using the first two cases.
        """
        if self.root is None:
            return
        if starting_node is None:
            starting_node = self.root

        # key < starting_node so we recurse left
        if key < starting_node.key:
            self.delete(key, starting_node.left)
        # key > starting_node so we recurse right
        elif key > starting_node.key:
            self.delete(key, starting_node.right)
        # starting_node is key and we can begin the deletion process.
        else:
            if starting_node.count > 1:
                starting_node.count -= 1
            # starting_node is a leaf
            elif starting_node.left is None and starting_node.right is None:
                if starting_node.parent is None:
                    self.root = None
                elif starting_node == starting_node.parent.left:
                    starting_node.parent.left = None
                else:
                    starting_node.parent.right = None
            # starting_node has both children
            elif starting_node.left != None and starting_node.right != None:
                succ = self.get(self.min_value(starting_node.right.key))
                starting_node.key = succ.key
                starting_node.data = succ.data
                # succ is a leaf
                # (succ cannot have a left child because it is the min)
                if succ.right is None:
                    # succ is a left child
                    if succ.parent.left == succ:
                        succ.parent.left = None
                    # succ is a right child
                    else:
                        succ.parent.right = None
                # succ has a right child
                else:
                    # succ is a left child
                    if succ.parent.left == succ:
                        succ.parent.left = succ.right
                        succ.right.parent = succ.parent
                    # succ is a right child
                    else:
                        succ.parent.right = succ.right
                        succ.right.parent = succ.parent
            # starting_node has one child
            else:
                if starting_node == self.root:
                    # Child is left
                    if starting_node.left != None:
                        starting_node.left.parent = None
                        self.root = starting_node.left
                    # Child is right
                    else:
                        starting_node.right.parent = None
                        self.root = starting_node.right
                # starting_node is left child:
                elif starting_node.parent.left == starting_node:
                    # Child is left
                    if starting_node.left != None:
                        starting_node.left.parent = starting_node.parent
                        starting_node.parent.left = starting_node.left
                    # Child is right
                    else:
                        starting_node.right.parent = starting_node.parent
                        starting_node.parent.left = starting_node.right
                # starting_node is right child
                else:
                    # Child is left
                    if starting_node.left != None:
                        starting_node.left.parent = starting_node.parent
                        starting_node.parent.right = starting_node.left
                    else:
                        starting_node.right.parent = starting_node.parent
                        starting_node.parent.right = starting_node.right

        # Update height of starting_node
        starting_node.height = max(
            starting_node.left.height if starting_node.left else 0,
            starting_node.right.height if starting_node.right else 0) + 1

        # Get balance factor
        balance = self.get_balance(starting_node)
        # Use balance factor to rotate

        # Left Left
        if balance > 1 and self.get_balance(starting_node.left) >= 0:
            self.right_rotate(starting_node)
        # Left Right
        if balance > 1 and self.get_balance(starting_node.left) < 0:
            self.left_rotate(starting_node.left)
            self.right_rotate(starting_node)
        # Right Right
        if balance < -1 and self.get_balance(starting_node.right) <= 0:
            self.left_rotate(starting_node)
        # Right Left
        if balance < -1 and self.get_balance(starting_node.right) > 0:
            self.right_rotate(starting_node.right)
            self.left_rotate(starting_node)

    def __delitem__(self, key):
        self.delete(key)


def traverse(rootnode: Node) -> None:
    """ Prints a map of the tree starting at rootnode """
    thislevel = [rootnode]
    while thislevel:
        nextlevel = list()
        row_string = ""
        for node in thislevel:
            if node.parent != None:
                if node.parent.left == node:
                    relation = "L"
                elif node.parent.right == node:
                    relation = "R"
            else:
                relation = "ro"
            row_string += str(node.key) + str((relation, node.data)) + " "
            if node.left:
                nextlevel.append(node.left)
            if node.right:
                nextlevel.append(node.right)
        print(row_string)
        thislevel = nextlevel


if __name__ == '__main__':
    TREE = AvlTree()
    TREE .insert(10)
    TREE .insert(20)
    TREE .insert(15)
    traverse(TREE .root)
