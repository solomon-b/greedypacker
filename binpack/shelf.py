#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""


class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, x, y) -> None:
        self.x = x if x > y else y
        self.y = y if y < x else x


    def __repr__(self):
        return 'Item(x=%r, y=%r)' % (self.x, self.y)


    def rotate(self) -> None:
        self.x, self.y = self.y, self.x


    def area(self) -> int:
        return self.x * self.y
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
        best_shelf = False
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
        best_shelf = False
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
        best_shelf = False
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
        worst_shelf = False
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
                return True
            if heuristic == 'next_fit':
                if self.next_fit(item):
                    return True
            elif heuristic == 'first_fit':
                if self.first_fit(item):
                    return True
            elif heuristic == 'best_width_fit':
                if self.best_width_fit(item):
                    return True
            elif heuristic == 'best_height_fit':
                if self.best_height_fit(item):
                    return True
            elif heuristic == 'best_area_fit':
                if self.best_area_fit(item):
                    return True
            elif heuristic == 'worst_width_fit':
                if self.worst_width_fit(item):
                    return True
            # No shelf fit but sheet fit
            if item.y <= self.available_height:
                new_shelf = Shelf(self.x, item.y)
                new_shelf.insert(item)
                self.shelves.append(new_shelf)
                return True
        # No sheet fit
        return False

if __name__ == '__main__':
    SHEET = Sheet(8, 5)
    ITEM = Item(2, 6)
    ITEM2 = Item(3, 2)
    ITEM3 = Item(1, 1)
    print(SHEET.insert(ITEM, heuristic='worst_width_fit'))
    print(SHEET.insert(ITEM2, heuristic='worst_width_fit'))
    print(SHEET.insert(ITEM3, heuristic='worst_width_fit'))
    print(SHEET)
    for i, shelf in enumerate(SHEET.shelves):
        print('Shelf #%s: %r' % (i, str(shelf.items)))
