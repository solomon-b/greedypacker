#!/usr/bin/env python
"""
BinManager

The main program interface for the package. BinPack manages
creation and ranking of bins and returns layout dictionaries
for packed bins.

"""
from functools import reduce
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
        self.bin_sel_algo = self._bin_best_fit
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
            self.algorithm = shelf.Sheet
            if heuristic in self.h_choices:
                self.heuristic = heuristic
                return True
            return False
        elif family == 'guillotine':
            self.algorithm = guillotine.Guillotine
            if heuristic in self.h_choices:
                self.heuristic = heuristic
                return True
            return False
        else:
            return False


    def _bin_first_fit(self, item: item.Item) -> None:
        """
        Insert into the first bin that fits the item
        """
        for binn in self.bins:
            result = binn.insert(item, self.heuristic)
            if result:
                break
        if not result:
            self.bins.append(self.algorithm(self.bin_width, self.bin_height))
            self.bins[-1].insert(item, self.heuristic)


    def _bin_best_fit(self, item: item.Item) -> None:
        """
        Insert into the bin that best fits the item
        """
        best_rect = None
        best_bin_index = None
        for i, binn in enumerate(self.bins):
            fitted_rects = [rect for rect
                            in binn.freerects
                            if rect.width >= item.x
                            and rect.height >= item.y]
            if fitted_rects:
                compare = lambda a, b: a if a.area > b.area else b
                best_in_bin = reduce(compare, fitted_rects)
                if best_in_bin:
                    if not best_rect:
                        best_rect = best_in_bin
                        best_bin_index = i
                    elif best_in_bin.width < best_rect.width:
                        best_rect = best_in_bin
                        best_bin_index = i
                    self.bins[i].insert(item, self.heuristic)
                    return
        self.bins.append(self.algorithm(self.bin_width, self.bin_height))
        self.bins[-1].insert(item, self.heuristic)
        return


    def execute(self) -> None:
        """
        Loop over all items and attempt insertion
        """
        self.bins = [self.algorithm(self.bin_width, self.bin_height)]
        for item in self.items:
            self.bin_sel_algo(item)


if __name__ == '__main__':
    MANAGER = BinManager()
    MANAGER.add_items(item.Item(2,6), item.Item(3,2), item.Item(1,1))
    MANAGER.set_algorthim('shelf', 'worst_width_fit')
    MANAGER.execute()
