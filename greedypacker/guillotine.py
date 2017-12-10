#!/usr/bin/env python
"""
Guillotine Style 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
import bisect
from typing import List, Tuple
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
                 heuristic: str = 'best_area_fit',
                 rectangle_merge: bool=True,
                 split_heuristic: str='default') -> None:
        self.x = x
        self.y = y
        self.area = self.x * self.y
        self.free_area = self.x * self.y
        self.rMerge = rectangle_merge
        self.split_heuristic = split_heuristic

        if heuristic == 'best_area':
            self._score = scoreBAF
        elif heuristic == 'best_shortside':
            self._score = scoreBSSF
        elif heuristic == 'best_longside':
            self._score = scoreBLSF
        elif heuristic == 'worst_area':
            self._score = scoreWAF
        elif heuristic == 'worst_shortside':
            self._score = scoreWSSF
        elif heuristic == 'worst_longside':
            self._score = scoreWLSF
        else:
            raise ValueError('No such heuristic!')

        if x == 0 or y == 0:
            #self.freerects = [] # type: List[FreeRectangle]
            self.freerects = SortedListWithKey(iterable=None, key=lambda x: x.area, load=1000)
        else:
            self.freerects = SortedListWithKey([FreeRectangle(self.x, self.y, 0, 0)], key=lambda x: x.area, load=1000)
        self.items = [] # type: List[Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Guillotine(%r)" % (self.items)


    @staticmethod
    def _item_fits_rect(item: Item,
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


    def _add_item(self, item: Item, x: int, y: int, rotate: bool = False) -> None:
        """ Helper method for adding items to the bin """
        if rotate:
            item.rotate()
        item.x, item.y = x, y
        self.items.append(item)
        self.free_area -= item.area


    def rectangle_merge(self) -> None:
        """
        Rectangle Merge optimization
        Finds pairs of free rectangles and merges them if they are mergable.
        """
        for freerect in self.freerects:
            widths_func = lambda r: (r.width == freerect.width and
                                     r.x == freerect.x and r != freerect)
            matching_widths = list(filter(widths_func, self.freerects))
            heights_func = lambda r: (r.height == freerect.height and
                                      r.y == freerect.y and r != freerect)
            matching_heights = list(filter(heights_func, self.freerects))
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


    def _find_best_score(self, item: Item):
        rects = []
        for rect in self.freerects:
            if self._item_fits_rect(item, rect):
                rects.append((self._score(rect, item), rect, False))
            if self.rotation and self._item_fits_rect(item, rect, rotation=True):
                rects.append((self._score(rect, item), rect, True))
        try:
            _score, rect, rot = min(rects, key=lambda x: x[0])
            return _score, rect, rot
        except ValueError:
            return None, None, False


    def insert(self, item: Item, heuristic: str = 'best_area') -> bool:
        """
        Add items to the bin. Public Method.
        """
        _, best_rect, rotated = self._find_best_score(item)
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


def scoreBAF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Area Fit """
    return rect.area-item.area, min(rect.width-item.width, rect.height-item.height)
        

def scoreBSSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Shortside Fit """
    return min(rect.width-item.width, rect.height-item.height), max(rect.width-item.width, rect.height-item.height)


def scoreBLSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Best Longside Fit """
    return max(rect.width-item.width, rect.height-item.height), min(rect.width-item.width, rect.height-item.height)


def scoreWAF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Area Fit """
    return (0 - (rect.area-item.area)), (0 - min(rect.width-item.width, rect.height-item.height))
        

def scoreWSSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Shortside Fit """
    return (0 - min(rect.width-item.width, rect.height-item.height)), (0 - max(rect.width-item.width, rect.height-item.height))


def scoreWLSF(rect: FreeRectangle, item: Item) -> Tuple[int, int]:
    """ Worst Longside Fit """
    return (0 - max(rect.width-item.width, rect.height-item.height)), (0 - min(rect.width-item.width, rect.height-item.height))
