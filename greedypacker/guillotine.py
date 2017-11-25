#!/usr/bin/env python
"""
Guillotine Style 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
import bisect
from typing import List
from functools import reduce
from collections import namedtuple
from sortedcontainers import SortedListWithKey # type: ignore
from .item import Item


class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):

    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


class Guillotine:
    def __init__(self, x: int = 8,
                 y: int = 4,
                 rotation: bool = True,
                 rectangle_merge: bool=True,
                 split_heuristic: str='default') -> None:
        self.x = x
        self.y = y
        self.area = self.x * self.y
        self.free_area = self.x * self.y
        self.rMerge = rectangle_merge
        self.split_heuristic = split_heuristic

        if x == 0 or y == 0:
            #self.freerects = [] # type: List[FreeRectangle]
            self.freerects = SortedListWithKey(iterable=None, key=lambda x: x.area, load=1000)
        else:
            self.freerects = SortedListWithKey([FreeRectangle(self.x, self.y, 0, 0)], key=lambda x: x.area, load=1000)
        self.items = [] # type: List[Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Guillotine(%r)" % (self.items)


    def _fitted_rects(self, item: Item,
                      rotation: bool = False) -> List[FreeRectangle]:
        """
        Returns a list of FreeRectangles that the item fits
        """
        width = item.width if not rotation else item.height
        height = item.height if not rotation else item.width
        return [rect for rect
                in self.freerects
                if rect.width >= width
                and rect.height >= height]


    @staticmethod
    def item_fits_rect(item: Item,
                       rect: FreeRectangle,
                       rotation: bool=False) -> bool:
        if (not rotation and
            item.width <= rect.width and 
            item.height <= rect.height):
            return True
        if (rotation and 
            item.height <= rect.width and 
            item.width <= rect.height):
            return True
        return False


    @staticmethod
    def _split_along_axis(freeRect: FreeRectangle,
                          item: Item, split: bool) -> List[FreeRectangle]:
        top_x = freeRect.x
        top_y = freeRect.y + item.height
        top_h = freeRect.height - item.height

        right_x = freeRect.x + item.width
        right_y = freeRect.y
        right_w = freeRect.width - item.width

        # horizontal split
        if split:
            top_w = freeRect.width
            right_h = item.height
        # vertical split
        else:
            top_w = item.width
            right_h = freeRect.height

        result = []

        if right_w > 0 and right_h > 0:
            right_rect = FreeRectangle(right_w, right_h, right_x, right_y)
            result.append(right_rect)

        if top_w > 0 and top_h > 0:
            top_rect = FreeRectangle(top_w, top_h, top_x, top_y)
            result.append(top_rect)
        return result


    def _split_free_rect(self, item: Item,
                         freeRect: FreeRectangle) -> List[FreeRectangle]:
        """
        Determines the split axis based upon the split heuristic then calls
        _split_along_axis  with the appropriate axis to return a List[FreeRectangle].
        """

        # Leftover lengths
        w = freeRect.width - item.width
        h = freeRect.height - item.height

        if self.split_heuristic == 'SplitShorterLeftoverAxis': split = (w <= h)
        elif self.split_heuristic == 'SplitLongerLeftoverAxis': split = (w > h)
        elif self.split_heuristic == 'SplitMinimizeArea': split = (item.width * h > w * item.height)
        elif self.split_heuristic == 'SplitMaximizeArea': split = (item.width * h <= w * item.height)
        elif self.split_heuristic == 'SplitShorterAxis': split = (freeRect.width <= freeRect.height)
        elif self.split_heuristic == 'SplitLongerAxis': split = (freeRect.width > freeRect.height)
        else: split = True


        return self._split_along_axis(freeRect, item, split)


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


    def _add_item(self, item: Item, x: int, y: int, rotate: bool = False) -> bool:
        """ Helper method for adding items to the bin """
        if rotate:
            item.rotate()
        item.x, item.y = x, y
        self.items.append(item)
        self.free_area -= item.area


    def best_shortside(self, item: Item) -> bool:
        """
        Pack Item into a FreeRectangle such that
        the smaller leftover side is minimized, ie:
        pick the FreeRectangle where min(Fw - Iw, Fh - Ih)
        is the smallest.
        """
        best_rect = None
        best_shortside = float('inf')
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            shortside = min(rect.width-item.width,
                            rect.height-item.height)
            if shortside < best_shortside:
                best_rect = rect
                best_shortside = shortside
                rotated = False

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                shortside = min(rect.width-item.height,
                                rect.height-item.width)
                if shortside < best_shortside:
                    best_rect = rect
                    best_shortside = shortside
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def best_longside(self, item: Item) -> bool:
        """
        Pack Item into a FreeRectangle such that
        the larger leftover side is minimized, ie:
        pick the FreeRectangle where max(Fw - Iw, Fh - Ih)
        is the smallest.
        """
        best_rect = None
        best_longside = float('inf')
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            longside = max(rect.width-item.width,
                           rect.height-item.height)
            if longside < best_longside:
                best_rect = rect
                best_longside = longside

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                longside = max(rect.width-item.height,
                           rect.height-item.width)
                if longside < best_longside:
                    best_rect = rect
                    best_longside = longside
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def best_area(self, item: Item) -> bool:
        """
        Insert item into rectangle with smallest
        area
        """
        best_rect = None
        best_area = float('inf')
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            area = rect.width*rect.height 
            if area < best_area:
                best_rect = rect
                best_area = area
                rotated = False

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                area = rect.width*rect.height 
                if area < best_area:
                    best_rect = rect
                    best_area = area
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def worst_shortside(self, item: Item) -> bool:
        """
        Pack Item into a FreeRectangle such that
        the smaller leftover side is minimized, ie:
        pick the FreeRectangle where min(Fw - Iw, Fh - Ih)
        is the greatest.
        """
        best_rect = None
        best_shortside = -1
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            shortside = min(rect.width-item.width,
                            rect.height-item.height)
            if shortside > best_shortside:
                best_rect = rect
                best_shortside = shortside
                rotated = False

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                shortside = min(rect.width-item.height,
                                rect.height-item.width)
                if shortside > best_shortside:
                    best_rect = rect
                    best_shortside = shortside
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def worst_longside(self, item: Item) -> bool:
        """
        Pack Item into a FreeRectangle such that
        the larger leftover side is minimized, ie:
        pick the FreeRectangle where max(Fw - Iw, Fh - Ih)
        is the greatest.
        """
        best_rect = None
        best_longside = -1
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            longside = max(rect.width-item.width,
                           rect.height-item.height)
            if longside > best_longside:
                best_rect = rect
                best_longside = longside

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                longside = max(rect.width-item.height,
                               rect.height-item.width)
                if longside > best_longside:
                    best_rect = rect
                    best_longside = longside
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def worst_area(self, item: Item) -> bool:
        """
        Insert item into rectangle with largest
        area
        """
        best_rect = None
        best_area = -1
        rotated = False
        for rect in self.freerects:
            if not self.item_fits_rect(item, rect):
                continue
            area = rect.width*rect.height 
            if area > best_area:
                best_rect = rect
                best_area = area
                rotated = False

        if self.rotation:
            for rect in self.freerects:
                if not self.item_fits_rect(item, rect, rotation=True):
                    continue
                area = rect.width*rect.height 
                if area > best_area:
                    best_rect = rect
                    best_area = area
                    rotated = True

        if best_rect:
            self._add_item(item, best_rect.x, best_rect.y, rotated)
            self.freerects.remove(best_rect)
            splits = self._split_free_rect(item, best_rect)
            for rect in splits:
                self.freerects.add(rect)
            if self.rMerge:
                self.rectangle_merge()
            return True
        return False


    def rectangle_merge(self) -> None:
        """
        Rectangle Merge optimization
        Finds pairs of free rectangles and merges them if they are mergable.
        """
        for freerect in self.freerects:
            matching_widths = list(filter(lambda r: (r.width == freerect.width and
                                                     r.x == freerect.x) and
                                                     r != freerect, self.freerects))
            matching_heights = list(filter(lambda r: (r.height == freerect.height and
                                                      r.y == freerect.y) and
                                                      r != freerect, self.freerects))
            if matching_widths:
                widths_adjacent = list(filter(lambda r: r.y == freerect.y + freerect.height, matching_widths)) # type: List[FreeRectangle]

                if widths_adjacent:
                    match_rect = widths_adjacent[0]
                    merged_rect = FreeRectangle(freerect.width,
                                                freerect.height+match_rect.height,
                                                freerect.x,
                                                freerect.y)
                    self.freerects.remove(freerect)
                    self.freerects.remove(match_rect)
                    self.freerects.add(merged_rect)

            if matching_heights:
                heights_adjacent = list(filter(lambda r: r.x == freerect.x + freerect.width, matching_heights))
                if heights_adjacent:
                    match_rect = heights_adjacent[0]
                    merged_rect = FreeRectangle(freerect.width+match_rect.width,
                                                freerect.height,
                                                freerect.x,
                                                freerect.y)
                    self.freerects.remove(freerect)
                    self.freerects.remove(match_rect)
                    self.freerects.add(merged_rect)


    def insert(self, item: Item, heuristic: str = 'best_area') -> bool:
        """
        Public method for selecting heuristic and inserting item
        """
        if heuristic == 'best_shortside':
            return self.best_shortside(item)
        elif heuristic == 'best_longside':
            return self.best_longside(item)
        elif heuristic == 'best_area':
            return self.best_area(item)
        elif heuristic == 'worst_shortside':
            return self.worst_shortside(item)
        elif heuristic == 'worst_longside':
            return self.worst_longside(item)
        elif heuristic == 'worst_area':
            return self.worst_area(item)
        else:
            return False


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.area,
            'efficiency': (self.area - self.free_area) / self.area,
            'items': self.items,
            }

        return stats
