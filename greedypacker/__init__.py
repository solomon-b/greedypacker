"""
Greedy Bin Packer

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

from .binmanager import BinManager
from .item import Item
