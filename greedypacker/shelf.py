#!/usr/bin/env python
"""
Shelf Style 2D Bin Algorithm and Data Structure

Solomon Bothwell
ssbothwell@gmail.com
"""
from functools import reduce
from typing import List
from . import item
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
        self.items = [] # type: List[item.Item]


    def __repr__(self):
        return str(self.__dict__)
        #return "Shelf(Available Width=%r, Height=%r, Vertical Offset=%r)" % (self.available_width, self.y, self.vertical_offset)


    def insert(self, item: item.Item, rotation: bool=True) -> bool:
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
    def __init__(self, x: int, y: int, rotation: bool = True, wastemap: bool = False) -> None:
        self.x = x
        self.y = y
        self.available_height = self.y
        self.shelves = []
        self.items = [] # type: List[item.Item]
        self.area = self.x * self.y
        self.free_area = self.x * self.y
        self.rotation = rotation
        self.use_waste_map = wastemap
        if self.use_waste_map:
            self.wastemap = guillotine.Guillotine(0, 0, rotation = self.rotation)


    def __repr__(self) -> str:
        return "Sheet(width=%s, height=%s, shelves=%s)" % (self.x, self.y, str(self.shelves))


    def create_shelf(self, item: item.Item) -> bool:
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


    def item_fits_shelf(self, item: item.Item, shelf: Shelf) -> bool:
        if ((item.width <= shelf.available_width and item.height <= shelf.y) or
           (self.rotation and item.height <= shelf.available_width and item.width <= shelf.y)):
            return True
        return False


    @staticmethod
    def rotate_to_shelf(item: item.Item, shelf: Shelf) -> bool:
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


    def add_to_shelf(self, item: item.Item, shelf: Shelf) -> bool:
        """ Item insertion helper method for heuristic methods """
        if not self.item_fits_shelf(item, shelf):
            return False
        if self.rotation:
            self.rotate_to_shelf(item, shelf)
        res = shelf.insert(item, self.rotation)
        if res:
            self.items.append(item)
            self.free_area -= item.area
            return True
        return False


    def add_to_wastemap(self, shelf: Shelf) -> None:
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


    def next_fit(self, item: item.Item) -> bool:
        open_shelf = self.shelves[-1]
        if self.item_fits_shelf(item, open_shelf):
            self.add_to_shelf(item, open_shelf)
            return True
        return False


    def first_fit(self, item: item.Item) -> bool:
        for shelf in self.shelves:
            if self.item_fits_shelf(item, shelf):
                self.add_to_shelf(item, shelf)
                return True
        return False


    def best_width_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_width = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.available_width - item.width < best_width:
                    best_width = shelf.available_width - item.width
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def best_height_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_height = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.y - item.height < best_height:
                    best_width = shelf.available_width - item.height
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def best_area_fit(self, item: item.Item) -> bool:
        best_shelf = None
        best_area = float('inf')
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                remainder_area = (shelf.available_width - item.width)*shelf.y
                if remainder_area < best_area:
                    best_area = remainder_area
                    best_shelf = shelf
        if best_shelf:
            self.add_to_shelf(item, best_shelf)
            return True
        return False


    def worst_width_fit(self, item: item.Item) -> bool:
        worst_shelf = None
        worst_width = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.available_width - item.width > worst_width:
                    worst_width = shelf.available_width - item.width
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def worst_height_fit(self, item: item.Item) -> bool:
        worst_shelf = None
        worst_height = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                if shelf.y - item.width > worst_height:
                    worst_height = shelf.available_width - item.width
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def worst_area_fit(self, item) -> bool:
        worst_shelf = None
        worst_area = 0
        for shelf in self.shelves:
            # Looks redundent but is to get optimal bestfit calc 
            self.rotate_to_shelf(item, shelf)
            if self.item_fits_shelf(item, shelf):
                remainder_area = (shelf.available_width - item.width)*shelf.y
                if remainder_area > worst_area:
                    worst_area = remainder_area
                    worst_shelf = shelf
        if worst_shelf:
            self.add_to_shelf(item, worst_shelf)
            return True
        return False


    def insert(self, item: item.Item, heuristic: 'str' = 'next_fit') -> bool:
        if (item.width <= self.x and item.height <= self.y):
            # 1) If there are no shelves, create one and insert the item
            if not self.shelves:
                return self.create_shelf(item)

            # 2) If enabled, try to insert into the wastemap 
            if self.use_waste_map:
                res = self.wastemap.insert(item, heuristic='best_area')
                if res:
                    self.items.append(item)
                    self.free_area -= item.area
                    return True

            # Ugly python switch statement
            heuristics = {'next_fit': self.next_fit,
                          'first_fit': self.first_fit,
                          'best_width_fit': self.best_width_fit,
                          'best_height_fit': self.best_height_fit,
                          'best_area_fit': self.best_area_fit,
                          'worst_width_fit': self.worst_width_fit,
                          'worst_height_fit': self.worst_height_fit,
                          'worst_area_fit': self.worst_area_fit }

            # 3) Try the desired heuristic
            if heuristic in heuristics:
                # Call Heuristic
                res = heuristics[heuristic](item)
                # If item inserted successfully
                if res:
                    return True
            # 4) If the item didn't fit then close the shelf
            #    and add its waste to the wastemap
            if self.use_waste_map:
                self.add_to_wastemap(self.shelves[-1])

                # 5) Attempt to insert into the wastemap
                res = self.wastemap.insert(item, heuristic='best_area')
                if res:
                    self.items.append(item)
                    self.free_area -= item.area
                    return True
            # 6) Attempt to create a new shelf for the item
            return self.create_shelf(item)
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
