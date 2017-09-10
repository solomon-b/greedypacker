#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""

from typing import NamedTuple, Tuple, List, Iterator, Dict
from itertools import product
from functools import reduce, partial


class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, x, y) -> None:
        self.x = x if x > y else y
        self.y = y if y < x else x


    def __repr__(self):
        return 'Item(x=%r, y=%r)' % (self.x, self.y)


    def rotate(self) -> bool:
        self.x, self.y = self.y, self.x


    def __lt__(self, other: 'Item') -> bool:
        return True if self.y < other.y else False


    def __le__(self, other: 'Item') -> bool:
        return True if self.y <= other.y else False


    def __eq__(self, other: 'Item') -> bool:
        return True if self.y == other.y else False


    def __ne__(self, other: 'Item') -> bool:
        return True if self.y != other.y else False


    def __gt__(self, other: 'Item') -> bool:
        return True if self.y > other.y else False


    def __ge__(self, other: 'Item') -> bool:
        return True if self.y >= other.y else False


class Shelf:
    """
    Shelf class represents of row of items on the sheet
    """
    def __init__(self, x: int, y: int) -> None:
        self.y = y
        self.x = x
        self.available_width = self.x
        self.items = [] # type: List[Item]


    def __lt__(self, other: 'Shelf') -> bool:
        return True if self.available_width < other.available_width  else False


    def __le__(self, other: 'Shelf') -> bool:
        return True if self.available_width  <= other.available_width  else False


    def __eq__(self, other: 'Shelf') -> bool:
        return True if self.available_width  == other.available_width  else False


    def __ne__(self, other: 'Shelf') -> bool:
        return True if self.available_width  != other.available_width  else False


    def __gt__(self, other: 'Shelf') -> bool:
        return True if self.available_width  > other.available_width  else False


    def __ge__(self, other: 'Shelf') -> bool:
        return True if self.available_width  >= other.available_width  else False


    def __repr__(self):
        return "Shelf(Available Width=%r, Height=%r)" % (self.available_width, self.y)


    def insert(self, item: Item) -> bool:
        if item.x <= self.available_width and item.y <= self.y:
            self.available_width -= item.x
            self.items.append(item)
            return True
        return False


    def check_item_fit(self, item: Item) -> bool:
        return item.y <= self.y and item.x <= self.available_width


    def check_reverse_item_fit(self, item: Item) -> bool:
        return item.x <= self.y and item.y <= self.available_width


    def item_best_fit(self, item: Item) -> int:
        """
        Find optimal item fit.
        1 = default, 2 = rotated, 0 = no fit
        """
        if self.check_item_fit(item) and self.check_reverse_item_fit(item):
            return 2 if item.x > item.y else 1
        elif self.check_item_fit(item):
            return 1
        elif self.check_reverse_item_fit(item):
            return 2
        else:
            return 0


class Sheet:
    """
    Sheet class represents a sheet of material to be subdivided.
    Sheets hold a list of rows which hold a list of items.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x if x > y else y
        self.y = y if y < x else x
        self.available_height = self.y
        self.shelves = [] # type: List[Shelf]


    def __repr__(self) -> str:
        return "Sheet(width=%s, height=%s, shelves=%s)" % (self.x, self.y, str(self.shelves))


    def next_fit(self, item: Item) -> bool:
        current_shelf = self.shelves[-1]
        fit_score = current_shelf.item_best_fit(item)
        # Optimal fit is default
        if fit_score == 1:
            current_shelf.insert(item)
            return True
        # Optimal fit is rotated
        elif fit_score == 2:
            item.rotate()
            current_shelf.insert(item)
            return True
        # No shelf fit but sheet fit
        elif item.y <= self.available_height:
            new_shelf = Shelf(self.x, item.y)
            new_shelf.insert(item)
            self.shelves.append(new_shelf)
            return True
        # No sheet fit
        return False


    def first_fit(self, item) -> bool:
        for shelf in self.shelves:
            fit_score = shelf.item_best_fit(item)
            if fit_score == 1:
                shelf.insert(item)
                return True
            elif fit_score == 2:
                item.rotate()
                shelf.insert(item)
                return True
        # No shelf fit but sheet fit
        if item.y <= self.available_height:
            new_shelf = Shelf(self.x, item.y)
            new_shelf.insert(item)
            self.shelves.append(new_shelf)
            return True
        # No sheet fit
        return False


    def best_width_fit(self, item) -> bool:
        best_shelf = False
        rotate = False
        for shelf in self.shelves:
            fit_score = shelf.item_best_fit(item)
            if fit_score == 1:
                if not best_shelf:
                    best_shelf = shelf
                elif shelf.available_width - item.x < best_shelf.available_width:
                    best_shelf = shelf
            elif fit_score == 2:
                if not best_shelf:
                    best_shelf = shelf
                    rotate = True
                elif shelf.available_width - item.y < best_shelf.available_width:
                    best_shelf = shelf
                    rotate = True

        if best_shelf:
            if rotate: item.rotate()
            best_shelf.insert(item)
            return True
        # No shelf fit but sheet fit
        if item.y <= self.available_height:
            new_shelf = Shelf(self.x, item.y)
            new_shelf.insert(item)
            self.shelves.append(new_shelf)
            return True
        # No sheet fit
        return False


    def best_height_fit(self, item) -> bool:
        best_shelf = False
        rotate = False
        for shelf in self.shelves:
            fit_score = shelf.item_best_fit(item)
            if fit_score == 1:
                if not best_shelf:
                    best_shelf = shelf
                elif shelf.y - item.y < best_shelf.y:
                    best_shelf = shelf
            elif fit_score == 2:
                if not best_shelf:
                    best_shelf = shelf
                    rotate = True
                elif shelf.y - item.x < best_shelf.y:
                    best_shelf = shelf
                    rotate = True

        if best_shelf:
            if rotate: item.rotate()
            best_shelf.insert(item)
            return True
        # No shelf fit but sheet fit
        if item.y <= self.available_height:
            new_shelf = Shelf(self.x, item.y)
            new_shelf.insert(item)
            self.shelves.append(new_shelf)
            return True
        # No sheet fit
        return False


    def best_area_fit(self, item) -> bool:
        best_shelf = False
        rotate = False
        for shelf in self.shelves:
            fit_score = shelf.item_best_fit(item)
            shelf_area = shelf.available_width * shelf.y
            item_area = item.x * item.y

            if fit_score:
                if not best_shelf:
                    best_shelf = shelf
                if shelf_area - item_area < (best_shelf.y *
                  best_shelf.available_width):
                    best_shelf = shelf
                if fit_score == 2: rotate = True

        if best_shelf:
            if rotate: item.rotate()
            best_shelf.insert(item)
            return True
        # No shelf fit but sheet fit
        if item.y <= self.available_height:
            new_shelf = Shelf(self.x, item.y)
            new_shelf.insert(item)
            self.shelves.append(new_shelf)
            return True
        # No sheet fit
        return False


    def insert(self, item: Item) -> bool:
        if item.x <= self.x and item.y <= self.y:
            if not self.shelves:
                new_shelf = Shelf(self.x, item.y)
                self.shelves.append(new_shelf)
                self.available_height -= new_shelf.y
                new_shelf.insert(item)
                return True
            else:
                self.best_area_fit(item)
                return True
        return False

if __name__ == '__main__':
    s = Sheet(8, 5)
    i = Item(3, 6)
    i2 = Item(2, 6)
    i3 = Item(1, 1)
    print(s.insert(i))
    print(s.insert(i2))
    print(s.insert(i3))
    print(s)
    for i, shelf in enumerate(s.shelves):
        print('Shelf #%s: %r' % (i, str(shelf.items)))
