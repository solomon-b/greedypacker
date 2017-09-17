#!/usr/bin/env python
"""
BinManager

The main program interface for the package. BinPack manages
creation and ranking of bins and returns layout dictionaries
for packed bins.

"""
from typing import List
from . import item
from . import shelf
from . import guillotine


class BinManager:
    """
    Interface Class.
    """
    def __init__(self, bin_width: int = 8, bin_height: int = 4) -> None:
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.items = []
        self.bins = []
        self.bin_count = 0
        self.algorithm = 'shelf'
        self.h_choices = ['next_fit',
                          'first_fit',
                          'best_width_fit',
                          'best_height_fit',
                          'best_area_fit',
                          'worst_width_fit'
                         ]
        self.heuristic = 'next_fit'


    def add_items(self, *items: List[item.Item]) -> bool:
        for item in items:
            self.items.append(item)
        self.items.sort(key=lambda el: el.x*el.y, reverse=True)


    def set_algorthim(self, family: str, heuristic: str) -> bool:
        if family == 'shelf':
            self.algorithm = shelf.Sheet(self.bin_width, self.bin_height)
            if heuristic in self.h_choices:
                self.heuristic = heuristic
                return True
            return False
        elif family == 'guillotine':
            self.algorithm = guillotine.Guillotine(self.bin_width,
                                                   self.bin_height)
            if heuristic in self.h_choices:
                self.heuristic = heuristic
                return True
            return False
        else:
            return False

    def execute(self) -> None:
        for item in self.items:
            self.algorithm.insert(item, self.heuristic)

        #for i, shelf in enumerate(self.algorithm.shelves):
        #    print('Shelf #%s: %r' % (i, str(shelf.items)))


if __name__ == '__main__':
    MANAGER = BinManager()
    MANAGER.add_items(item.Item(2,6), item.Item(3,2), item.Item(1,1))
    MANAGER.set_algorthim('shelf', 'worst_width_fit')
    MANAGER.execute()
