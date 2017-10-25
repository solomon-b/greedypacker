#!/usr/bin/env python
"""
Maximal Rectangle 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
from typing import List, Tuple, Union
from functools import reduce
from collections import namedtuple
from . import item


class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


class MaximalRectangle:
    def __init__(self, x: int = 8,
                 y: int = 4,
                 rotation: bool = True,
                 rectangle_merge: bool=False,
                 split_heuristic: str='default') -> None:
        self.x = x
        self.y = y
        self.rMerge = rectangle_merge
        self.split_heuristic = split_heuristic


        if x == 0 or y == 0:
            self.freerects = [] # type: List[FreeRectangle]
        else:
            self.freerects = [FreeRectangle(self.x, self.y, 0, 0)] # type: List[FreeRectangle]
        self.items = [] # type: List[item.Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "MaximalRectangle(%r)" % (self.items)


    @staticmethod
    def item_fits_rect(item: item.Item, rect: FreeRectangle) -> bool:
        if ((item.width <= rect.width and item.height <= rect.height) or
           (item.height <= rect.width and item.width <= rect.height)):
            return True
        return False


    @staticmethod
    def checkInstersection(usedRect: FreeRectangle,
                           freeRect: FreeRectangle) -> bool:
        """ 
        Checks if two rectangles intersect
        """

        # Check if nodes actually intersect
        if (usedRect.x >= freeRect.x + freeRect.width or 
            usedRect.x + usedRect.width <= freeRect.x or 
            usedRect.y >= freeRect.y + freeRect.height or
            usedRect.y + usedRect.height <= freeRect.y):
            return False
        return True
        

    @staticmethod
    def findOverlap(F1: FreeRectangle, F2: FreeRectangle) -> tuple:
        """
        returns the bottom left and top right 
        coordinates of the overlap
        """
        X1, Y1 = F1.x, F1.y
        X2, Y2 = F1.x+F1.width, F1.y+F1.height
        X3, Y3 = F2.x, F2.y
        X4, Y4 = F2.x+F2.width, F2.y+F2.height

        X5 = max(X1, X3)
        Y5 = max(Y1, Y3)
        X6 = min(X2, X4)
        Y6 = min(Y2, Y4)

        return (X5, Y5, X6, Y6)

    @staticmethod
    def clipOverlap(rect: FreeRectangle,
                         overlap: tuple) -> List[FreeRectangle]:
        """
        Return maximal rectangles for  non-intersected 
        parts of rect.
        """
        Fx, Fy = rect.x, rect.y
        Fw, Fh = rect.width, rect.height
        Ox1, Oy1, Ox2, Oy2 = overlap
                
        results = []
        
        ## Check for non-intersected sections
        # Left Side
        if Ox1 > Fx:
            L = FreeRectangle(width=Ox1-Fx, height=Fh, x=Fx, y=Fy)
            results.append(L)
        # Right side
        if Ox2 < Fx + Fw:
            R = FreeRectangle(width=(Fx+Fw)-Ox2, height=Fh, x=Ox2, y=Fy)
            results.append(R)
        # Bottom Side
        if Oy1 > Fy:
            B = FreeRectangle(width=Fw, height=Oy1-Fy, x=Fx, y=Fy)
            results.append(B)
        # Top Side
        if Oy2 < Fy + Fh:
            T = FreeRectangle(width=Fw, height=(Fy+Fh)-Oy2, x=Fx, y=Oy2)
            results.append(T)

        return results
       
        

    def first_fit(self, item: item.Item) -> bool:
        """
        Select first indexed FreeRectangle (that fits item)
        """
        
        for el in self.freerects:
            if el[0] and self.item_fits_rect(item, el[0]):
                item.CornerPoint = el[0].x, el[0].y
                intersection = self.findIntersection(el)

                self.freerects = filter(lambda F: F != el, self.freerects)
                return self.freerects
            elif el[1] and self.item_fits_rect(item, el[1]):
                item.CornerPoint = el[1].x, el[1].y
                self.freerects = filter(lambda F: F != el, self.freerects)
                return self.freerects
        return False
                

        if not fitted_rects and self.rotation:
            fitted_rects = self._fitted_rects(item, rotation=True)
            if fitted_rects:
                item.rotate()
        for freerect in fitted_rects:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(freerect)

            splits = self._split_free_rect(item, freerect)
            for rect in splits:
                self.freerects.append(rect)
            return True
        return False


if __name__ == '__main__':
    M = MaximalRectangle(0, 0)
    F0 = FreeRectangle(2,4,2,0)
    F1 = FreeRectangle(4,2,0,2)
    F2 = FreeRectangle(4,2,4,2)
    F3 = FreeRectangle(2,4,6,0)
    I = item.Item(2,4)
    M.freerects.append((F0, F1))
    M.freerects.append((F2, F3))
    #print(list(M.first_fit(I)))
    print(M.findoverlap((F1, F0)))
