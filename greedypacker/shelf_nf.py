#!/usr/bin/env python
"""
Next Fit Shelf Algorithm

This is a reimplimentation (with slight modifactions) of
Jukka Jylänki's C++ version available here:
https://github.com/juj/RectangleBinPack/blob/master/ShelfNextFitBinPack.cpp

Solomon Bothwell
ssbothwell@gmail.com
"""
from . import item

class ShelfNextFit:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.currentX = 0
        self.currentY = 0
        self.shelfHeight = 0
        self.usedSurfaceArea = 0

    def insert(self, item: item.Item) -> bool:
        """
        1. First item in a shelf should maximize width.
        2. Further items should maximize height if possible.
        """
        if ((item.x > item.y and item.x < self.shelfHeight) or
           (item.y < item.x and item.y > self.shelfHeight)):
            item.rotate()

        # Item is too big for current shelf
        if self.currentX + item.x > self.width:
            self.currentX = 0
            self.currentY += self.shelfHeight
            self.shelfHeight = 0

            # Store long edge horizontally when starting a shelf
            if item.x < item.y:
                item.rotate()

        if item.x > self.width or self.currentY + item.y > self.height:
            item.rotate()
            if item.x > self.width or self.currentY + item.y > self.height:
                return False
        item.CornerPoint = (self.currentX, self.currentY)
        self.currentX += item.x
        self.shelfHeight = max(self.shelfHeight, item.y)
        self.usedSurfaceArea += item.y*item.x
        return True

    def insert_norotate(self, item: item.Item) -> bool:
        """
        No rotations version
        """
        if self.currentX + item.x > self.width:
            self.currentX = 0
            self.currentY += self.shelfHeight
            self.shelfHeight = 0
        if self.currentX + item.x > self.width or self.currentY + item.y > self.height:
            return False
        item.CornerPoint = (self.currentX, self.currentY)
        self.currentX += item.x
        self.shelfHeight = max(self.shelfHeight, item.y)
        self.usedSurfaceArea += item.y*item.x
        return True

