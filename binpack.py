#!/usr/bin/env python
"""
Bin Pack

A two dimensional binpacking algorithm with options
for first fit and best fit greedy heuristics.

Bins are represented using a custom tree structure called a
BinTree. BinTrees are ranked using a modified AVL tree called
BinRank. Each Bintree is associated with an AVL node. Nodes
are ranked by the BinTree's largest unoccupied node.

BinTrees and corresponding IDs are stored in a dict. AVL
Node payloads hold IDs and Node keys are the BinTree's max
unoccupied scores.
"""
from collections import deque
from operator import mul as product
import avl_tree, bintree

class BinPack:
    """
    Bin Ranking System. the product of BinTree.largest_child
    is used as a key value in an AVL Tree for ranking the bins.
    """
    def __init__(self, bin_size: tuple = (4, 8), sorting: bool = True):
        self.bin_dict = {}
        self.bin_size = bin_size
        self.tree = avl_tree.AvlTree()
        self.bin_count = 0
        self.sorting = sorting
        self._add_bin()


    def _add_bin(self) -> None:
        """
        private method. Creates a new BinTree and adds
        it to bin_dict and the AVL tree.
        """
        self.bin_dict[self.bin_count] = bintree.BinTree(width=self.bin_size[0], height=self.bin_size[1])
        bin_key = product(*self.bin_dict[self.bin_count].largest_child)
        self.tree.insert(bin_key)
        self.tree[bin_key].data.append(self.bin_count)
        self.bin_count += 1


    def insert(self, *items: tuple, heuristic: str = 'best_fit') -> None:
        if self.sorting == True:
            items = sorted(items, key=lambda a: product(*a), reverse=True)

        for item in items:
            if heuristic == 'best_fit':
                self.best_fit(item)
            elif heuristic == 'next_fit':
                self.next_fit(item)


    def best_fit(self, item_dims: tuple) -> bool:
        """
        First Fit Bin Selection
        Public method.
        Selects optimal BinTree (or creates
        a new BinTree) for item insertion using first fit.
        Returns BinTree ID.
        """
        item_area = product(*item_dims)
        item = bintree.Item(*item_dims)
        queue = deque([self.tree.root])
        best_fit = None
        best_fit_node = None
        while queue:
            current_node = queue.popleft()
            current_bintree = self.bin_dict[current_node.data[-1]]
            largest_child = current_bintree.largest_child
            if (largest_child[0] >= item.width and
                    largest_child[1] >= item.height):
                if not best_fit or largest_child < best_fit.largest_child:
                    best_fit = current_bintree
                    best_fit_node = current_node
                if current_node.left:
                    queue.append(current_node.left)
            else:
                if current_node.right:
                    queue.append(current_node.right)
        if best_fit:
            best_fit.insert(item)
            # delete and reinsert node to update position in tree
            nodeid = best_fit_node.data[-1]
            old_key = best_fit_node.key
            new_key = product(*best_fit.largest_child)
            self.tree.delete(key=old_key)
            self.tree.insert(key=new_key)
            self.tree[new_key].data.append(nodeid)
            return True
        else:
            self._add_bin()
            self.bin_dict[self.bin_count-1].insert(item)
            #avl_tree.traverse(self.tree.root)
            #print("...")
            return True


    def next_fit(self, item_dims: tuple) -> bool:
        """
        First Fit Bin Selection
        Public method.
        Selects optimal BinTree (or creates
        a new BinTree) for item insertion using first fit.
        Returns BinTree ID.
        """
        item_area = product(*item_dims)
        item = bintree.Item(*item_dims)
        queue = deque([self.tree.root])
        while queue:
            current_node = queue.popleft()
            current_bintree = self.bin_dict[current_node.data[-1]]
            largest_child = current_bintree.largest_child
            if (largest_child[0] >= item.width and
                    largest_child[1] >= item.height):
                current_bintree.insert(item)
                # delete and reinsert node to update position in tree
                nodeid = current_node.data[-1]
                old_key = current_node.key
                new_key = product(*current_bintree.largest_child)
                self.tree.delete(key=old_key)
                self.tree.insert(key=new_key)
                self.tree[new_key].data.append(nodeid)
                return True
            else:
                if current_node.right:
                    queue.append(current_node.right)
                else:
                    self._add_bin()
                    self.next_fit(item_dims)
        return False


    def print_stats(self) -> None:
        """
        Returns layouts for all BinTrees
        """
        for key, bin in self.bin_dict.items():
            bintree.bin_stats(bin)

if __name__ == '__main__':
    BINPACK = BinPack(bin_size=(4,8))
    BINPACK.insert((2, 4), (2, 2), (4, 5), (4, 4), (2, 2), (3, 2), heuristic='next_fit')
    BINPACK.print_stats()
