#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
from functools import reduce
from . import item


class Shelf:
    """
    Shelf class represents of row of items on the sheet
    """
    def __init__(self, x: int, y: int, v_offset: int = 0) -> None:
        self.y = y
        self.x = x
        self.available_width = self.x
        self.vertical_offset = v_offset
        self.items = [] # type: List[item.Item]


    def __repr__(self):
        return str(self.__dict__)
        #return "Shelf(Available Width=%r, Height=%r, Vertical Offset=%r)" % (self.available_width, self.y, self.vertical_offset)


    def insert(self, item: item.Item) -> bool:
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
    def __init__(self, x: int, y: int, rotation: bool = True) -> None:
        self.x = x if x > y else y
        self.y = y if y < x else x
        self.available_height = self.y
        self.shelves = [] # type: List[Shelf]
        self.items = [] # type: List[item.Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Sheet(width=%s, height=%s, shelves=%s)" % (self.x, self.y, str(self.shelves))


    def next_fit(self, item: item.Item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if self.rotation:
            fitted_shelves_rotated = [shelf for shelf
                                      in self.shelves
                                      if shelf.available_width >= item.y
                                      and shelf.y >= item.x]
        if fitted_shelves:
            current_shelf = fitted_shelves[-1]
            current_shelf.insert(item)
            self.items.append(item)
            return True
        elif fitted_shelves_rotated:
            current_shelf = fitted_shelves_rotated[-1]
            item.rotate()
            current_shelf.insert(item)
            self.items.append(item)
            return True
        return False


    def first_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if self.rotation:
            fitted_shelves_rotated = [shelf for shelf
                                      in self.shelves
                                      if shelf.available_width >= item.y
                                      and shelf.y >= item.x]
        if fitted_shelves:
            current_shelf = fitted_shelves[0]
            current_shelf.insert(item)
            self.items.append(item)
            return True
        elif fitted_shelves_rotated:
            current_shelf = fitted_shelves_rotated[0]
            item.rotate()
            current_shelf.insert(item)
            self.items.append(item)
            return True
        return False


    def best_width_fit(self, item: item.Item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if not fitted_shelves and self.rotation:
            fitted_shelves = [shelf for shelf in self.shelves if shelf.available_width >= item.y and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if (a.available_width < b.available_width) else b, fitted_shelves)
        best_shelf.insert(item)
        self.items.append(item)
        return True


    def best_height_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if not fitted_shelves and self.rotation:
            fitted_shelves = [shelf for shelf
                              in self.shelves
                              if shelf.available_width >= item.y
                              and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if (a.y < b.y) else b, fitted_shelves)
        best_shelf.insert(item)
        self.items.append(item)
        return True


    def best_area_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if not fitted_shelves and self.rotation:
            fitted_shelves = [shelf for shelf
                              in self.shelves
                              if shelf.available_width >= item.y
                              and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        best_shelf = reduce(lambda a, b: a if ((a.y * a.available_width) < (b.y * b.available_width)) else b, fitted_shelves)
        best_shelf.insert(item)
        self.items.append(item)
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
        self.items.append(item)
        return True


    def worst_height_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if not fitted_shelves and self.rotation:
            fitted_shelves = [shelf for shelf
                              in self.shelves
                              if shelf.available_width >= item.y
                              and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        worst_shelf = reduce(lambda a, b: a if (a.y > b.y) else b, fitted_shelves)
        worst_shelf.insert(item)
        self.items.append(item)
        return True


    def worst_area_fit(self, item) -> bool:
        fitted_shelves = [shelf for shelf
                          in self.shelves
                          if shelf.available_width >= item.x
                          and shelf.y >= item.y]
        if not fitted_shelves and self.rotation:
            fitted_shelves = [shelf for shelf
                              in self.shelves
                              if shelf.available_width >= item.y
                              and shelf.y >= item.x]
            if fitted_shelves:
                item.rotate()
            else:
                return False
        worst_shelf = reduce(lambda a, b: a if ((a.y * a.available_width) > (b.y * b.available_width)) else b, fitted_shelves)
        worst_shelf.insert(item)
        self.items.append(item)
        return True


    def insert(self, item: item.Item, heuristic: 'str' = 'next_fit') -> bool:
        if item.x <= self.x and item.y <= self.y:
            if not self.shelves:
                new_shelf = Shelf(self.x, item.y)
                self.shelves.append(new_shelf)
                self.available_height -= new_shelf.y
                new_shelf.insert(item)
                self.items.append(item)
                return True

            heuristics = {'next_fit': self.next_fit,
                          'first_fit': self.first_fit,
                          'best_width_fit': self.best_width_fit,
                          'best_height_fit': self.best_height_fit,
                          'best_area_fit': self.best_area_fit,
                          'worst_width_fit': self.worst_width_fit,
                          'worst_height_fit': self.worst_height_fit,
                          'worst_area_fit': self.worst_area_fit }

            if heuristic in heuristics:
                # Call Heuristic
                res = heuristics[heuristic](item)
                # If item inserted successfully
                if res:
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
            'efficiency': sum([i.x*i.y for i in self.items])/(self.x*self.y),
            'items': self.items,
            }

        return stats

if __name__ == '__main__':
    SHEET = Sheet(8, 5)
    ITEM = item.Item(2, 6)
    ITEM2 = item.Item(3, 2)
    ITEM3 = item.Item(1, 1)
    ITEM4 = item.Item(4, 2)
    ITEM5 = item.Item(1, 8)
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
