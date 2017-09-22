#!/usr/bin/env python
"""
BinManager

The main program interface for the package. BinPack manages
creation and ranking of bins and returns layout dictionaries
for packed bins.

"""
from functools import reduce
from typing import List, Union, Callable
from . import item
from . import shelf
from . import guillotine

# Type Aliases:
Algorithm = Union[shelf.Sheet, guillotine.Guillotine]


class BinManager:
    """
    Interface Class.
    """
    def __init__(self, bin_width: int = 8,
                 bin_height: int = 4,
                 bin_algo: str = 'bin_best_fit',
                 pack_algo: str = 'guillotine',
                 heuristic: str ='best_width_fit',
                 sorting: bool = True,
                 rotation: bool = True) -> None:
        self.bin_width = bin_width
        self.bin_height = bin_height
        self.items = [] # type: List[item.Item]
        self.bin_count = 0
        if bin_algo == 'bin_best_fit':
            self.bin_sel_algo = self._bin_best_fit
        elif bin_algo == 'bin_first_fit':
            self.bin_sel_algo =  self._bin_first_fit
        self.heuristic = heuristic
        self.algorithm = pack_algo
        defaultBin = self._bin_factory(self.bin_width,
                                           self.bin_height,
                                           self.algorithm,
                                           self.heuristic) # type: Algorithm
        self.bins = [defaultBin] # type: List[Algorithm]
        self.sorting = sorting
        self.rotation = rotation


    def add_items(self, *items: item.Item) -> bool:
        for item in items:
            self.items.append(item)
        if self.sorting:
            self.items.sort(key=lambda el: el.x*el.y, reverse=True)


    def _bin_factory(self, width: int, height: int, algo: str, heuristic: str) -> Algorithm:
        """
        Returns a bin with the desired algorithm,
        heuristic, and dimensions
        """
        if algo == 'guillotine':
            return guillotine.Guillotine(width, height)
        elif algo == 'shelf':
            return shelf.Sheet(width, height)
        return


    def _bin_first_fit(self, item: item.Item) -> None:
        """
        Insert into the first bin that fits the item
        """
        for binn in self.bins:
            result = binn.insert(item, self.heuristic)
            if result:
                break
        if not result:
            self.bins.append(self._bin_factory(self.bin_width,
                                               self.bin_height,
                                               self.algorithm,
                                               self.heuristic))
            self.bins[-1].insert(item, self.heuristic)


    def _bin_best_fit(self, item: item.Item) -> None:
        """
        Insert into the bin that best fits the item
        """
        if item.x > self.bin_width or item.y > self.bin_height:
            return "Error! item too big for bins"

        best_rect = None # type: Union[guillotine.FreeRectangle, shelf.Shelf]
        best_bin_index = None # type: int
        if self.algorithm == 'guillotine':
            for i, binn in enumerate(self.bins):
                fitted_rects = [rect for rect
                                in binn.freerects
                                if rect.width >= item.x
                                and rect.height >= item.y]
                if fitted_rects:
                    compare = lambda a, b: a if a.area > b.area else b
                    best_in_bin = reduce(compare, fitted_rects)
                    if not best_rect:
                        best_rect = best_in_bin
                        best_bin_index = i
                    elif best_in_bin.width < best_rect.width:
                        best_rect = best_in_bin
                        best_bin_index = i

            if best_rect:
                self.bins[i].insert(item, self.heuristic)
                return


        if self.algorithm == 'shelf':
            bin_scores = [] # type: List[tuple]
            for i, binn in enumerate(self.bins):
                if binn.shelves == []:
                    bin_scores.append((binn.x - item.x, i))
                else:
                    fitted_shelves = [shelf for shelf
                                      in binn.shelves
                                      if shelf.available_width >= item.x
                                      and shelf.y >= item.y]
                    # This checks rotation fits if no regular fits.
                    # Need to compare regular fit and rotate fitted
                    # to find actual best fit
                    if not fitted_shelves and self.rotation:
                        fitted_shelves = [shelf for shelf
                                          in binn.shelves
                                          if shelf.available_width >= item.y
                                          and shelf.y >= item.x]
                        if fitted_shelves:
                            item.rotate()
                    if fitted_shelves:
                        compare = lambda a, b: a if (a.available_width <
                                                     b.available_width) else b
                        best_shelf = reduce(compare, fitted_shelves)
                        bin_scores.append((best_shelf.available_width - item.x, i))
                    elif binn.available_height >= item.y:
                        bin_scores.append((binn.x - item.x, i))
            if bin_scores:
                best_bin_index = min(bin_scores)[1]
                self.bins[best_bin_index].insert(item, self.heuristic)
                return
        self.bins.append(self._bin_factory(self.bin_width,
                                           self.bin_height,
                                           self.algorithm,
                                           self.heuristic))
        self.bins[-1].insert(item, self.heuristic)
        return


    def execute(self) -> None:
        """
        Loop over all items and attempt insertion
        """
        for item in self.items:
            self.bin_sel_algo(item)
