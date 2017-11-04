#!/usr/bin/env python
"""
BinManager

The main program interface for the package. BinPack manages
creation and ranking of bins and returns layout dictionaries
for packed bins.

"""
from functools import reduce
from typing import List, Union, Callable, Optional
from . import item
from . import shelf
from . import guillotine
from . import maximal_rectangles

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
                 heuristic: str ='default',
                 split_heuristic: str = 'default',
                 sorting: bool = True,
                 rotation: bool = True,
                 rectangle_merge: bool = True,
                 wastemap: bool = True) -> None:
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

        self.split_heuristic = split_heuristic
        self.sorting = sorting
        self.rotation = rotation
        self.rectangle_merge = rectangle_merge
        self.wastemap = wastemap

        defaultBin = self._bin_factory() # type: Algorithm
        self.bins = [defaultBin] # type: List[Algorithm]


    def add_items(self, *items: item.Item) -> None:
        for item in items:
            self.items.append(item)
        if self.sorting:
            self.items.sort(key=lambda el: el.width*el.height, reverse=True)


    def _bin_factory(self) -> Optional[Algorithm]:
        """
        Returns a bin with the specificed algorithm,
        heuristic, and dimensions
        """
        if self.algorithm == 'guillotine':
            return guillotine.Guillotine(self.bin_width, self.bin_height, self.rotation,
                                         self.rectangle_merge, self.split_heuristic)
        elif self.algorithm == 'shelf':
            return shelf.Sheet(self.bin_width, self.bin_height, self.rotation, self.wastemap)
        elif self.algorithm == 'maximal_rectangle':
            return shelf.maximal_rectangles.MaximalRectangle(self.bin_width, self.bin_height, self.rotation)
        raise ValueError('Error: No such Algorithm')


    def _bin_first_fit(self, item: item.Item) -> None:
        """
        Insert into the first bin that fits the item
        """
        result = False
        for binn in self.bins:
            result = binn.insert(item, self.heuristic)
            if result:
                break
        if not result:
            self.bins.append(self._bin_factory())
            self.bins[-1].insert(item, self.heuristic)


    def _bin_best_fit(self, item: item.Item) -> str:
        """
        Insert into the bin that best fits the item
        """

        # Ensure item can theoretically fit the bin
        item_fits = False
        if item.width <= self.bin_width or item.height >= self.bin_height:
            item_fits = True
        if self.rotation and (item.height <= self.bin_width or item.width >= self.bin_height):
            item_fits = True
        if not item_fits:
            return "Error! item too big for bin"


        best_rect = None # type: Union[guillotine.FreeRectangle, shelf.Shelf]
        best_bin_index = None # type: int
        if self.algorithm == 'guillotine':
            for i, binn in enumerate(self.bins):
                fitted_rects = [rect for rect
                                in binn.freerects
                                if rect.width >= item.width
                                and rect.height >= item.height]
                if fitted_rects:
                    compare = lambda x: x.area
                    best_in_bin = min(fitted_rects, key=compare)
                    if not best_rect:
                        best_rect = best_in_bin
                        best_bin_index = i
                    elif best_in_bin.width < best_rect.width:
                        best_rect = best_in_bin
                        best_bin_index = i

            if best_rect:
                self.bins[i].insert(item, self.heuristic)
                return "Success"


        if self.algorithm == 'shelf':
            bin_scores = [] # type: List[tuple]
            for i, binn in enumerate(self.bins):
                if binn.shelves == []:
                    bin_scores.append((binn.x - item.width, i))
                else:
                    fitted_shelves = [shelf for shelf
                                      in binn.shelves
                                      if shelf.available_width >= item.width
                                      and shelf.y >= item.height]
                    # This checks rotation fits if no regular fits.
                    # Need to compare regular fit and rotate fitted
                    # to find actual best fit
                    if not fitted_shelves and self.rotation:
                        fitted_shelves = [shelf for shelf
                                          in binn.shelves
                                          if shelf.available_width >= item.height
                                          and shelf.y >= item.width]
                        if fitted_shelves:
                            item.rotate()
                    if fitted_shelves:
                        compare = lambda a, b: a if (a.available_width <
                                                     b.available_width) else b
                        best_shelf = reduce(compare, fitted_shelves)
                        bin_scores.append((best_shelf.available_width - item.width, i))
                    elif binn.available_height >= item.height:
                        bin_scores.append((binn.x - item.width, i))
            if bin_scores:
                best_bin_index = min(bin_scores)[1]
                self.bins[best_bin_index].insert(item, self.heuristic)
                return "success"
        self.bins.append(self._bin_factory())
        self.bins[-1].insert(item, self.heuristic)
        return "Success"


    def execute(self) -> None:
        """
        Loop over all items and attempt insertion
        """
        for item in self.items:
            self.bin_sel_algo(item)
