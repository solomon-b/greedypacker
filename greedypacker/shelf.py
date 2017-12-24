#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
#from functools import reduce
from typing import List, Tuple
from .item import Item
from . import guillotine


class Shelf:
    """
    Shelf class represents of row of items on the sheet
    """
    def __init__(self, x: int, y: int, v_offset: int = 0) -> None:
        self.y = y
        self.x = x
        self.available_width = self.x
        self.area = self.available_width * self.y
        self.vertical_offset = v_offset
        self.items = [] # type: List[Item]


    def __repr__(self):
        return str(self.__dict__)
        #return "Shelf(Available Width=%r, Height=%r, Vertical Offset=%r)" % (self.available_width, self.y, self.vertical_offset)


    def insert(self, item: Item, rotation: bool=True) -> bool:
        if item.width <= self.available_width and item.height <= self.y:
            item.x, item.y = (self.x - self.available_width, self.vertical_offset)
            self.items.append(item)
            self.available_width -= item.width
            self.area = self.available_width * self.y
            return True
        if rotation:
            if (item.height <= self.available_width and
                item.width <= self.y):
                item.rotate()
                item.x, item.y = (self.x - self.available_width, self.vertical_offset)
                self.items.append(item)
                self.available_width -= item.width
                self.area = self.available_width * self.y
                return True
        return False


class Sheet:
    """
    Sheet class represents a sheet of material to be subdivided.
    Sheets hold a list of rows which hold a list of items.
    """
    def __init__(self, x: int, y: int, rotation: bool = True, 
                 wastemap: bool = False, heuristic: str = 'best_area_fit') -> None:
        self.x = x
        self.y = y
        self.available_height = self.y
        self.shelves = []
        self.items = [] # type: List[Item]
        self.area = self.x * self.y
        self.free_area = self.x * self.y
        self.rotation = rotation
        self.use_waste_map = wastemap
        if self.use_waste_map:
            self.wastemap = guillotine.Guillotine(0, 0, rotation = self.rotation, heuristic='best_area')

        if heuristic == 'best_width_fit':
            self._score = scoreBWF
        elif heuristic == 'best_height_fit':
            self._score = scoreBHF
        elif heuristic == 'best_area_fit':
            self._score = scoreBAF
        elif heuristic == 'worst_width_fit':
            self._score = scoreWWF
        elif heuristic == 'worst_height_fit':
            self._score = scoreWHF
        elif heuristic == 'worst_area_fit':
            self._score = scoreWAF
        elif heuristic == 'next_fit':
            self._score = scoreNF
        elif heuristic == 'first_fit':
            self._score = scoreFF
        else:
            raise ValueError('No such heuristic!')

    def __repr__(self) -> str:
        return "Sheet(width=%s, height=%s, available_height=%s, shelves=%s)" % (self.x, self.y, self.available_height, str(self.shelves))


    def _create_shelf(self, item: Item) -> bool:
        if (self.rotation and item.height > item.width and
           item.height < self.x and item.width < self.y):
            item.rotate()
        if item.height <= self.available_height:
            v_offset = self.y - self.available_height
            new_shelf = Shelf(self.x, item.height, v_offset)
            self.shelves.append(new_shelf)
            self.available_height -= new_shelf.y
            new_shelf.insert(item)
            self.items.append(item)
            self.free_area -= item.area
            return True
        return False


    def _item_fits_shelf(self, item: Item, shelf: Shelf, rotation: bool = False) -> bool:
        if ((item.width <= shelf.available_width and item.height <= shelf.y) or
           (rotation and item.height <= shelf.available_width and item.width <= shelf.y)):
            return True
        return False


    @staticmethod
    def _rotate_to_shelf(item: Item, shelf: Shelf) -> bool:
        """
        Rotate item to long side vertical if that orientation
        fits the shelf.
        """
        if (item.width > item.height and
            item.width <= shelf.y and
            item.height <= shelf.available_width):
            item.rotate()
            return True
        return False


    def _add_to_shelf(self, item: Item, shelf: Shelf) -> bool:
        """ Item insertion helper method for heuristic methods """
        if not self._item_fits_shelf(item, shelf):
            return False
        if self.rotation:
            self._rotate_to_shelf(item, shelf)
        res = shelf.insert(item, self.rotation)
        if res:
            self.items.append(item)
            self.free_area -= item.area
            return True
        return False


    def _add_to_wastemap(self, shelf: Shelf) -> None:
        """ Add lost space above items to the wastemap """
        # Add space above items to wastemap
        for item in shelf.items:
            if item.height < shelf.y:
                freeWidth = item.width
                freeHeight = shelf.y - item.height
                freeX = item.x
                freeY = item.height + shelf.vertical_offset
                freeRect = guillotine.FreeRectangle(freeWidth,
                                                    freeHeight,
                                                    freeX,
                                                    freeY)
                self.wastemap.freerects.add(freeRect)
        # Move remaining shelf width to wastemap
        if shelf.available_width > 0:
            freeWidth = shelf.available_width
            freeHeight = shelf.y
            freeX = self.x - shelf.available_width
            freeY = shelf.vertical_offset
            freeRect = guillotine.FreeRectangle(freeWidth,
                                                freeHeight,
                                                freeX,
                                                freeY)
            self.wastemap.freerects.add(freeRect)
        # Close Shelf
        shelf.available_width = 0
        # Merge rectangles in wastemap
        self.wastemap.rectangle_merge()


    def _find_best_score(self, item: Item) -> Tuple[int, Shelf, bool]:
        """
        Score all the shelves and return the best
        one in a tuple with its score and if the item
        needs to be rotated. If the bin has no shelves
        and the item fits the available space, then
        give it a max score (0) with no shelves.
        """
        shelves = []
        if not self.shelves:
            return 0, None, False
        for shelf in self.shelves:
            if self._item_fits_shelf(item, shelf):
                shelves.append((self._score(shelf, item, self), shelf, False))
            if self._item_fits_shelf(item, shelf, rotation=True):
                shelves.append((self._score(shelf, item, self), shelf, True))

        # Give max score if item fits sheet but there are no shelves
        if not shelves and self.available_height >= item.height:
            shelves.append(((0, 0), None, False))
        if not shelves and self.available_height >= item.width and self.rotation:
            shelves.append(((0, 0), None, True))

        try:
            _score, shelf, rot = min(shelves, key=lambda x: x[0])
            return _score, shelf, rot
        except ValueError:
            return None, None, False


    def insert(self, item: Item, heuristic: 'str' = 'best_width') -> bool:
        if (item.width <= self.x and item.height <= self.y):
            # 1) If there are no shelves, create one and insert the item
            if not self.shelves:
                return self._create_shelf(item)

            # 2) If enabled, try to insert into the wastemap 
            if self.use_waste_map:
                res = self.wastemap.insert(item, heuristic='best_area')
                if res:
                    self.items.append(item)
                    self.free_area -= item.area
                    return True

            # 3) Try the desired heuristic
            if heuristic == 'first_fit':
                res = self.first_fit(item)
                if res:
                    return True
            else:
                _, best_shelf, rotated = self._find_best_score(item)
                if best_shelf:
                    if rotated:
                        item.rotate()
                    self._add_to_shelf(item, best_shelf)
                    return True

            # 4) If the item didn't fit then close the shelf
            #    and add its waste to the wastemap
            if self.use_waste_map:
                self._add_to_wastemap(self.shelves[-1])

                # 5) Attempt to insert into the wastemap
                res = self.wastemap.insert(item, heuristic='best_area')
                if res:
                    self.items.append(item)
                    self.free_area -= item.area
                    return True
            # 6) Attempt to create a new shelf for the item
            return self._create_shelf(item)
        # 7) Nothing worked!
        return False


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.area,
            'efficiency': (self.area-self.free_area)/self.area,
            'items': self.items,
            }

        return stats


def scoreBAF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Best Area Fit """
    return (shelf.available_width - item.width)*shelf.y, shelf.available_width - item.width


def scoreBHF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Best Height Fit """
    return shelf.y - item.height, shelf.available_width - item.width


def scoreBWF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Best Width Fit """
    return shelf.available_width - item.width, shelf.y - item.height


def scoreWAF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Worst Area Fit """
    return (0 - ((shelf.available_width - item.width)*shelf.y)), (0 - (shelf.available_width - item.width))


def scoreWHF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Worst Height Fit """
    return (0 - (shelf.y - item.height)), (0 - (shelf.available_width - item.width))


def scoreWWF(shelf: Shelf, item: Item, self=None) -> Tuple[int, int]:
    """ Worst Width Fit """
    return (0 - (shelf.available_width - item.width)), (0 - (shelf.y - item.height))


def scoreFF(shelf: Shelf, item: Item, self=None) -> Tuple[int, Shelf, bool]:
    """ First Fit """
    if self.shelves:
        for shelf in self.shelves:
            if self._item_fits_shelf(item, shelf):
                return (0, shelf, False)
            if self.rotation and self._item_fits_shelf(item, shelf, True):
                return (0, shelf, True)
    return (0, None, False)


def scoreNF(shelf: Shelf, item: Item, self=None) -> Tuple[int, Shelf, bool]:
    """ Next Fit """
    if self.shelves:
        open_shelf = self.shelves[-1]
        if self._item_fits_shelf(item, open_shelf):
            return (0, open_shelf, False)
        if self.rotation and self._item_fits_shelf(item, open_shelf, True):
            return (0, open_shelf, True)
    return (0, None, False)
