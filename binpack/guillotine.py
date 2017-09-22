#!/usr/bin/env python
"""
Guillotine Style 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
from typing import Optional, List, Callable
from functools import reduce
from collections import namedtuple
from . import item


class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


class Guillotine:
    def __init__(self, x: int = 8, y: int = 4, rotation: bool = True) -> None:
        self.x = x
        self.y = y
        self.rMerge = False
        self.freerects = [FreeRectangle(self.x, self.y, 0, 0)] # type: List[FreeRectangle]
        self.items = [] # type: List[item.Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Guillotine(%r)" % (self.items)


    def _fitted_rects(self, item: item.Item,
                      rotation: bool = False) -> List[FreeRectangle]:
        """
        Returns a list of FreeRectangles that the item fits
        """
        width = item.x if not rotation else item.y
        height = item.y if not rotation else item.x
        return [rect for rect
                in self.freerects
                if rect.width >= width
                and rect.height >= height] # type: List[FreeRectangle]

    def _split_free_rect(self, item: item.Item,
                         freerect: FreeRectangle,
                         split_axis: str = 'horiz') -> List[FreeRectangle]:
        """
        returns a list of FreeRectangles remaining after the split
        """
        result = []
        if item.x < freerect.width:
            # generate free rectangle for remaining width
            right_width = freerect.width - item.x
            right_height = item.y
            right_x = freerect.x + item.x
            right_y = freerect.y
            right_rect = FreeRectangle(right_width,
                                       right_height,
                                       right_x,
                                       right_y)
            result.append(right_rect)
        if item.y < freerect.height:
            top_width = freerect.width
            top_height = freerect.height - item.y
            top_x = freerect.x
            top_y = item.y + item.CornerPoint[1]
            top_rect = FreeRectangle(top_width,
                                     top_height,
                                     top_x,
                                     top_y)
            result.append(top_rect)
        return result


    @staticmethod
    def _rectangle_reduce(fitted_rects: List[FreeRectangle],
                          op = operator.lt,
                          field: str = 'width') -> FreeRectangle:
        """
        Reduces a list of FreeRectangles and returns the result
        """
        if fitted_rects:
            if field == 'width':
                compare = lambda a, b: a if op(a.width, b.width) else b
            if field == 'height':
                compare = lambda a, b: a if op(a.height, b.height) else b
            if field == 'area':
                compare = lambda a, b: a if op(a.area, b.area) else b
            return reduce(compare, fitted_rects)
        return None


    @staticmethod
    def _compare_two_freerects(A: FreeRectangle, B: FreeRectangle) -> FreeRectangle:
        """
        Returns the smaller of two FreeRectangles
        """
        if not A and not B:
            return None
        if A and B:
            return min(A, B)
        if A and not B:
            return A
        else:
            return B


    def first_fit(self, item: item.Item) -> bool:
        """
        Select first indexed FreeRectangle (that fits item)
        """
        fitted_rects = self._fitted_rects(item)
        if not fitted_rects and self.rotation:
            fitted_rects = self._fitted_rects(item, rotation=True)
            if fitted_rects:
                item.rotate()
        for freerect in fitted_rects:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(freerect)

            splits = self._split_free_rect(item, freerect)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def best_width_fit(self, item: item.Item) -> bool:
        """
        Select FreeRectangle with width closest to item.width
        """
        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.le, 'width')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot)
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            # Update Item Position
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            # Update self.freerects
            self.freerects.remove(best)
            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def best_height_fit(self, item) -> bool:
        """
        Select FreeRectangle with height closest to item.height
        """
        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.le, 'height')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot,
                                                      operator.le,
                                                      'height')
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            self.freerects.remove(best)

            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def best_area_fit(self, item) -> bool:
        """
        Select FreeRectangle with area closest to item.area
        """
        smallest_rect = None # type: FreeRectangle
        smallest_rotated = None # type: FreeRectangle
        best = None # type: FreeRectangle

        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.le, 'area')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot,
                                                      operator.le,
                                                      'area')
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            self.freerects.remove(best)
            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def worst_width_fit(self, item) -> bool:
        """
        Select FreeRectangle with width greatest compared to item.width
        """
        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.gt, 'width')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot,
                                                      operator.gt,
                                                      'width')
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            self.freerects.remove(best)
            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def worst_height_fit(self, item) -> bool:
        """
        Select FreeRectangle with height greatest compared to item.height
        """
        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.gt, 'height')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot,
                                                      operator.gt,
                                                      'height')
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            self.freerects.remove(best)
            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def worst_area_fit(self, item) -> bool:
        """
        Select FreeRectangle with area greatest compared to item.area
        """
        fitted_rects = self._fitted_rects(item)
        smallest_rect = self._rectangle_reduce(fitted_rects, operator.gt, 'area')

        if self.rotation:
            fitted_rects_rot = self._fitted_rects(item, rotation=True)
            smallest_rotated = self._rectangle_reduce(fitted_rects_rot,
                                                      operator.gt,
                                                      'area')
            best = self._compare_two_freerects(smallest_rect, smallest_rotated)
        else:
            best = smallest_rect

        if best:
            item.CornerPoint = (best.x, best.y)
            self.items.append(item)
            self.freerects.remove(best)
            splits = self._split_free_rect(item, best)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


    def rectangle_merge(self) -> None:
        """
        Rectangle Merge optimization
        Finds pairs of free rectangles and merges them if they are mergable.
        """
        for freerect in self.freerects:
            matching_widths = list(filter(lambda r: (r.width == freerect.width and
                                                     r.x == freerect.x) and r != freerect, self.freerects) # type: List[FreeRectangle]
                                                     )
            matching_heights = list(filter(lambda r: (r.height == freerect.height and
                                                      r.y == freerect.y) and r != freerect, self.freerects)) # type: List[FreeRectangle]

            if matching_widths:
                widths_adjacent = list(filter(lambda r: r.y == freerect.y + freerect.height, self.freerects)) # type: List[FreeRectangle]

                if widths_adjacent:
                    match_rect = widths_adjacent[0]
                    merged_rect = FreeRectangle(freerect.width,
                                                freerect.height+match_rect.height,
                                                freerect.x,
                                                freerect.y)
                    self.freerects.remove(freerect)
                    self.freerects.remove(match_rect)
                    self.freerects.append(merged_rect)

            if matching_heights:
                heights_adjacent = list(filter(lambda r: r.x == freerect.x + freerect.width, self.freerects))
                if heights_adjacent:
                    match_rect = heights_adjacent[0]
                    merged_rect = FreeRectangle(freerect.width+match_rect.width,
                                                freerect.height,
                                                freerect.x,
                                                freerect.y)
                    self.freerects.remove(freerect)
                    self.freerects.remove(match_rect)
                    self.freerects.append(merged_rect)


    def insert(self, item: item.Item, heuristic: str = 'best_area_fit') -> bool:
        """
        Public method for selecting heuristic and inserting item
        """
        heuristics = {'first_fit': self.first_fit,
                      'best_width_fit': self.best_width_fit,
                      'best_height_fit': self.best_height_fit,
                      'best_area_fit': self.best_area_fit,
                      'worst_width_fit': self.worst_width_fit,
                      'worst_height_fit': self.worst_height_fit,
                      'worst_area_fit': self.worst_area_fit}

        if heuristic in heuristics:
            # Call Heuristic
            res = heuristics[heuristic](item)
            # If item inserted successfully
            if res:
                if self.rMerge:
                    self.rectangle_merge()
                return True
        return False


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.x * self.y,
            'efficiency': 1-(sum([F.width*F.height for F in self.freerects])/(self.x*self.y)),
            'items': self.items,
            }

        return stats

if __name__ == '__main__':
    G = Guillotine(8, 4)
    I = item.Item(2, 5) # type: item.Item
    I2 = item.Item(2, 5) # type: item.Item
    I3 = item.Item(2, 2) # type: item.Item
    G.insert(I)
    G.insert(I2)
    G.insert(I3)
    print(G.bin_stats())
