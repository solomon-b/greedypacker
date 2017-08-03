#!/usr/bin/env python
"""
BinTree Class:

2 dimensional Bin Packing Data Structure

BinTrees have right and bottom children. Items
are inserted using recursion to find the first
open BinTree unoccupied node large enough to fit
them Item. That node is resized to match the Item
and child nodes are created to fill the unused
space to the left.

Example:
    Item := (2,4)
    Tree := ((4,8), occoupied == False)

    After Insertion:
    Tree :=     ((2,4), occupied == True)
                /                     \
      ((4,4), occupied == False)  ((2,4), occupied == False)

Items are namedtuples with x and y values. When
Items are inserted into a bin tree, insert()
recurses over child nodes until it finds the first
unoccupied node that fits the Item. The node is
resized to Item and two child nodes are created
to take up the remaining space to the right and
below the item.
"""

from typing import NamedTuple
from collections import deque

class CornerPoint(NamedTuple):
    """
    namedtuple representing the top left corner of each
    BinTree object.
    """
    x: int
    y: int


class Item(NamedTuple):
    """
    namedtuple representing objects added to BinTree.
    """
    width: int
    height: int


class BinTree:
    """
    Each BinTree instance has two children (left and bottom)
    and width (int), height (int), and occupied (bool) properties.
    """
    def __init__(self, width: int = 4, height: int = 8) -> None:
        self.corner = CornerPoint(0, 0)
        self.width = width
        self.height = height
        self.occupied = False
        self.parent = None
        self.right = None
        self.bottom = None
        if not self.occupied:
            self.largest_child = (self.width, self.height)
        else:
            self.largest_child = None


    def insert(self, item: Item) -> bool:
        """
        Recursive item insertion
        Takes an Item namedtuple
        Inserts recursively as a side-effect
        Returns True or False if Item fit in bin
        """
        if not self.occupied and item.width <= self.width and item.height <= self.height:
            if self.height - item.height > 0:
                self.bottom = BinTree(width=self.width, height=self.height-item.height)
                self.bottom.parent = self
            if self.width - item.width > 0:
                self.right = BinTree(width=self.width-item.width, height=item.height)
                self.right.parent = self
            self.height, self.width = item.height, item.width
            self.occupied = item
            if self.right:
                self.right.corner = CornerPoint(self.width + self.corner.x, self.corner.y)
            if self.bottom:
                self.bottom.corner = CornerPoint(self.corner.x, self.height + self.corner.y)
            self.calc_largest_child()
            return True
        else:
            if (self.right and self.right.largest_child[0] >= item.width and
                    self.right.largest_child[1] >= item.height):
                self.right.insert(item)
            elif (self.bottom and self.bottom.largest_child[0] >= item.width and
                  self.bottom.largest_child[1] >= item.height):
                self.bottom.insert(item)
            else:
                return False


    def calc_largest_child(self) -> None:
        """
        Updates self.largest_child for each node recursively
        back to the root node
        """
        choices = []
        if not self.occupied:
            choices.append((self.width, self.height))
        else:
            choices.append((0, 0))
        if self.right:
            choices.append(self.right.largest_child)
        else:
            choices.append((0, 0))
        if self.bottom:
            choices.append(self.bottom.largest_child)
        else:
            choices.append((0, 0))
        self.largest_child = max(choices, key=lambda t: t[0]*t[1])

        if self.parent:
            self.parent.calc_largest_child()


def bin_stats(root: BinTree) -> dict:
    """
    Returns a dictionary with compiled stats on the bin tree
    """
    stats = {
                'width': 0,
                'height': 0,
                'area': 0,
                'efficiency': 1.0,
                'items': [],
            }

    stack = deque([root])
    while stack:
        node = stack.popleft()
        stats['width'] += node.width
        if node.right:
            stack.append(node.right)

    stack = deque([root])
    while stack:
        node = stack.popleft()
        stats['height'] += node.height
        if node.bottom:
            stack.append(node.bottom)

    stats['area'] = stats['width'] * stats['height']

    stack = deque([root])
    occupied = 0
    while stack:
        node = stack.popleft()
        if node.occupied:
            stats['items'].append((node.corner, node.occupied))
            occupied += node.width*node.height

        if node.right:
            stack.append(node.right)
        if node.bottom:
            stack.append(node.bottom)
    stats['efficiency'] = occupied / stats['area']
    print(stats)
    return stats


if __name__ == '__main__':
    ROOT = BinTree()
    ITEM1 = Item(width=4, height=4)
    ITEM2 = Item(width=2, height=4)
    ITEM3 = Item(width=2, height=2)
    ITEM4 = Item(width=2, height=2)
    ROOT.insert(ITEM1)
    ROOT.insert(ITEM2)
    ROOT.insert(ITEM3)
    ROOT.insert(ITEM4)
    bin_stats(ROOT)
