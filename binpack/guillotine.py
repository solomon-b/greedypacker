#!/usr/bin/env python
"""
Guillotine Style 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
from item import Item


class Guillotine:
    def __init__(self, x: int = 8, y: int = 4) -> None:
        self.x = y
        self.y = y
        self.freerects = [] # type: List[tuple]
        self.items = [] # type: List[Item]


    def __repr__(self) -> None:
        return "Guillotine(%r)" % (self.items)


    def next_fit(self, item: Item) -> bool:
        pass

    def first_fit(self, item) -> bool:
        pass


    def _loop_result_helper(self, flag_shelf, rotate, item):
        pass


    def best_width_fit(self, item) -> bool:
        pass


    def best_height_fit(self, item) -> bool:
        pass


    def best_area_fit(self, item) -> bool:
        pass


    def worst_width_fit(self, item) -> bool:
        pass


    def __insert__(self, item: Item) -> bool:
        pass


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """
        pass

if __name__ == '__main__':
    G = Guillotine()
    print(G)
