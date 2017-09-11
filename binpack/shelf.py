#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
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


    def _loop_result_helper(self, flag_shelf, rotate, item):
        if flag_shelf:
            if rotate:
                item.rotate()
            flag_shelf.insert(item)
            return True
        return False


    def best_width_fit(self, item) -> bool:
        best_shelf = False # type: Any
        rotate = False
        for current_shelf in self.shelves:
            fit_score = current_shelf.item_best_fit(item)
            if fit_score == 1:
                if not best_shelf:
                    best_shelf = current_shelf
                elif current_shelf.available_width - item.x < best_shelf.available_width:
                    best_shelf = current_shelf
            elif fit_score == 2:
                if not best_shelf:
                    best_shelf = current_shelf
                    rotate = True
                elif current_shelf.available_width - item.y < best_shelf.available_width:
                    best_shelf = current_shelf
                    rotate = True
        return self._loop_result_helper(best_shelf, rotate, item)


    def best_height_fit(self, item) -> bool:
        best_shelf = False # type: Any
        rotate = False
        for current_shelf in self.shelves:
            fit_score = current_shelf.item_best_fit(item)
            if fit_score == 1:
                if not best_shelf:
                    best_shelf = current_shelf
                elif current_shelf.y - item.y < best_shelf.y:
                    best_shelf = current_shelf
            elif fit_score == 2:
                if not best_shelf:
                    best_shelf = current_shelf
                    rotate = True
                elif current_shelf.y - item.x < best_shelf.y:
                    best_shelf = current_shelf
                    rotate = True

        return self._loop_result_helper(best_shelf, rotate, item)


    def best_area_fit(self, item) -> bool:
        best_shelf = False # type: Any
        rotate = False
        for current_shelf  in self.shelves:
            fit_score = current_shelf.item_best_fit(item)
            shelf_area = current_shelf.available_width * current_shelf .y
            item_area = item.x * item.y

            if fit_score:
                if not best_shelf:
                    best_shelf = current_shelf
                if shelf_area - item_area < (best_shelf.y *
                                             best_shelf.available_width):
                    best_shelf = current_shelf
                if fit_score == 2:
                    rotate = True

        return self._loop_result_helper(best_shelf, rotate, item)


    def worst_width_fit(self, item) -> bool:
        worst_shelf = False # type: Any
        rotate = False
        for current_shelf in self.shelves:
            fit_score = current_shelf.item_best_fit(item)
            if fit_score == 1:
                if not worst_shelf:
                    worst_shelf = current_shelf
                elif current_shelf.available_width - item.x > worst_shelf.available_width:
                    worst_shelf = current_shelf
            elif fit_score == 2:
                if not worst_shelf:
                    worst_shelf = current_shelf
                    rotate = True
                elif current_shelf.available_width - item.y > worst_shelf.available_width:
                    worst_shelf = current_shelf
                    rotate = True

        return self._loop_result_helper(worst_shelf, rotate, item)


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
