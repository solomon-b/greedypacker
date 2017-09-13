#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
from functools import reduce
from item import Item


class Shelf:
    """
    Shelf class represents of row of items on the sheet
    """
    def __init__(self, x: int, y: int, v_offset: int = 0) -> None:
        self.y = y
        self.x = x
        self.available_width = self.x
        self.vertical_offset = v_offset
        self.items = [] # type: List[Item]


    def __lt__(self, other: 'Shelf') -> bool:
        return True if self.available_width < other.available_width else False


    def __le__(self, other: 'Shelf') -> bool:
        return True if self.available_width <= other.available_width else False


    def __eq__(self, other: 'Shelf') -> bool:
        return True if self.available_width == other.available_width else False


    def __ne__(self, other: 'Shelf') -> bool:
        return True if self.available_width != other.available_width else False


    def __gt__(self, other: 'Shelf') -> bool:
        return True if self.available_width > other.available_width else False


    def __ge__(self, other: 'Shelf') -> bool:
        return True if self.available_width >= other.available_width else False


    def __repr__(self):
        return "Shelf(Available Width=%r, Height=%r)" % (self.available_width, self.y)


    def insert(self, item: Item) -> bool:
        if item.x <= self.available_width and item.y <= self.y:
            self.available_width -= item.x
            item_length = len(self.items)
            if item_length == 0:
                item.CornerPoint = (0, self.vertical_offset)
            elif item_length == 1:
                item.CornerPoint = (self.items[0].x, self.vertical_offset)
            else:
                item.CornerPoint = (self.items[-1].CornerPoint[0] +
                                    self.items[-1].x, self.vertical_offset)
            self.items.append(item)
            return True
        return False


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
        self.items = [] # type: List[Item]


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


    def first_fit(self, item) -> bool:
        for current_shelf in self.shelves:
            fit_score = current_shelf.item_best_fit(item)
            if fit_score == 1:
                current_shelf.insert(item)
                return True
            elif fit_score == 2:
                item.rotate()
                current_shelf .insert(item)
                return True


    def best_width_fit(self, item: Item) -> bool:
        fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.x and shelf.y >= item.y]
        if not fitted_shelves:
            fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.y and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if (a.available_width < b.available_width) else b, fitted_shelves)
        best_shelf.insert(item)
        return True


    def best_height_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.x and shelf.y >= item.y]
        if not fitted_shelves:
            fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.y and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if (a.y < b.y) else b, fitted_shelves)
        best_shelf.insert(item)
        return True


    def best_area_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.x and shelf.y >= item.y]
        if not fitted_shelves:
            fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.y and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if ((a.y * a.available_width) < (b.y * b.available_width)) else b, fitted_shelves)
        best_shelf.insert(item)
        return True


    def worst_width_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.x and shelf.y >= item.y]
        if not fitted_shelves:
            fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.y and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if (a.available_width > b.available_width) else b, fitted_shelves)
        best_shelf.insert(item)
        return True


    def insert(self, item: Item, heuristic: 'str' = 'next_fit') -> bool:
        if item.x <= self.x and item.y <= self.y:
            if not self.shelves:
                new_shelf = Shelf(self.x, item.y)
                self.shelves.append(new_shelf)
                self.available_height -= new_shelf.y
                new_shelf.insert(item)
                self.items.append(item)
                return True
            if heuristic == 'next_fit':
                if self.next_fit(item):
                    self.items.append(item)
                    return True
            elif heuristic == 'first_fit':
                if self.first_fit(item):
                    self.items.append(item)
                    return True
            elif heuristic == 'best_width_fit':
                if self.best_width_fit(item):
                    self.items.append(item)
                    return True
            elif heuristic == 'best_height_fit':
                if self.best_height_fit(item):
                    self.items.append(item)
                    return True
            elif heuristic == 'best_area_fit':
                if self.best_area_fit(item):
                    self.items.append(item)
                    return True
            elif heuristic == 'worst_width_fit':
                if self.worst_width_fit(item):
                    self.items.append(item)
                    return True
            # No shelf fit but sheet fit
            if item.y <= self.available_height:
                if len(self.shelves) == 1:
                    v_offset = self.shelves[0].y
                else:
                    last_shelf = self.shelves[-1]
                    v_offset = last_shelf.vertical_offset + last_shelf.y

                new_shelf = Shelf(self.x, item.y, v_offset=v_offset)
                new_shelf.insert(item)
                self.shelves.append(new_shelf)
                self.items.append(item)
                self.available_height -= item.y
                return True
        # No sheet fit
        return False


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.x * self.y,
            'efficiency': sum([i.x*i.y for i in SHEET.items])/(self.x*self.y),
            'items': self.items,
            }

        return stats

if __name__ == '__main__':
    SHEET = Sheet(8, 5)
    ITEM = Item(2, 6)
    ITEM2 = Item(3, 2)
    ITEM3 = Item(1, 1)
    ITEM4 = Item(4, 2)
    ITEM5 = Item(1, 8)
    SHEET.insert(ITEM, heuristic='worst_width_fit')
    SHEET.insert(ITEM2, heuristic='worst_width_fit')
    SHEET.insert(ITEM3, heuristic='worst_width_fit')
    SHEET.insert(ITEM4, heuristic='worst_width_fit')
    SHEET.insert(ITEM5, heuristic='worst_width_fit')
    print(SHEET)
    print()
    for i, shelf in enumerate(SHEET.shelves):
        print('Shelf #%s: %r' % (i, str(shelf.items)))
    print()
    print(SHEET.bin_stats())
