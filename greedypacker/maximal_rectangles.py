#!/usr/bin/env python
"""
Maximal Rectangle 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import typing
from typing import List, Tuple, Union
from functools import reduce
from collections import namedtuple
from .item import Item


class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


class MaximalRectangle:
    def __init__(self, x: int = 8,
                 y: int = 4,
                 rotation: bool = True) -> None:
        self.x = x
        self.y = y
        self.area = self.x * self.y
        self.free_area = self.area


        if x == 0 or y == 0:
            self.freerects = [] # type: List[FreeRectangle]
        else:
            self.freerects = [FreeRectangle(self.x, self.y, 0, 0)] # type: List[FreeRectangle]
        self.items = [] # type: List[Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "MaximalRectangle(%r)" % (self.items)


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
    def _split_rectangle(rectangle: FreeRectangle,
                        item: Item) -> List[FreeRectangle]:
        """
        Return a list of maximal free rectangles from a split
        """
        results = []
        if item.width < rectangle.width:
            Fw = rectangle.width - item.width
            Fh = rectangle.height
            Fx = rectangle.x + item.width
            Fy = rectangle.y
            results.append(FreeRectangle(width=Fw,
                                         height=Fh,
                                         x=Fx,
                                         y=Fy))
        if item.height < rectangle.height:
            Fw = rectangle.width
            Fh = rectangle.height - item.height
            Fx = rectangle.x 
            Fy = rectangle.y + item.height
            results.append(FreeRectangle(width=Fw,
                                         height=Fh,
                                         x=Fx,
                                         y=Fy))
        return results
    

    @staticmethod
    def _item_bounds(item: Item) -> tuple:
        """
        Returns the lower left and upper right 
        corners of the item's bounding box.
        """
        return (item.x,
                item.y,
                item.x+item.width,
                item.y+item.height)


    @staticmethod
    def _check_intersection(free_rect: FreeRectangle,
                           bounding_box: tuple) -> bool:
        """ 
        Checks if bounding box intersects rectangle
        """

        # Check if nodes actually intersect
        if (bounding_box[0] >= free_rect.x + free_rect.width or
            bounding_box[2] <= free_rect.x or
            bounding_box[1] >= free_rect.y + free_rect.height or
            bounding_box[3] <= free_rect.y):
            return False
        return True
        

    @staticmethod
    def _find_overlap(F1: FreeRectangle, F2: tuple ) -> tuple:
        """
        returns the bottom left and top right 
        coordinates of the overlap
        """
        X1, Y1 = F1.x, F1.y
        X2, Y2 = F1.x+F1.width, F1.y+F1.height
        X3, Y3 = F2[0], F2[1]
        X4, Y4 = F2[2], F2[3]

        X5 = max(X1, X3)
        Y5 = max(Y1, Y3)
        X6 = min(X2, X4)
        Y6 = min(Y2, Y4)

        return (X5, Y5, X6, Y6)

    @staticmethod
    def _clip_overlap(rect: FreeRectangle,
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
       
        
    @staticmethod
    def _encapsulates(F0: FreeRectangle,
                     F1: FreeRectangle) -> bool:
        """
        Returns true if F1 is fully encapsulated
        inside F0
        """
        if F1.x < F0.x or F1.x > F0.x+F0.width:
            return False
        if F1.x+F1.width > F0.x+F0.width:
            return False
        if F1.y < F0.y or F1.y > F0.y+F0.height:
            return False
        if F1.y+F1.height > F0.y+F0.height:
            return False
        return True


    def _remove_redundent(self) -> List[FreeRectangle]:
        """
        Remove all FreeRectangles full encapsulated
        inside another FreeRectangle.
        """
        i = 0
        while i < len(self.freerects):
            j = i + 1
            while j < len(self.freerects):
                if self._encapsulates(self.freerects[j], self.freerects[i]):
                    del self.freerects[i]
                    i -= 1
                    break
                if self._encapsulates(self.freerects[i], self.freerects[j]):
                    del self.freerects[j]
                    j -= 1
                j += 1
            i += 1
        return self.freerects


    def _prune_overlaps(self, itemBounds: tuple) -> None:
        """
        Loop through all FreeRectangles and prune
        any overlapping the itemBounds
        """
        result = [] # type: List[FreeRectangle]
        for rect in self.freerects:
            if self._check_intersection(rect, itemBounds):
                overlap = self._find_overlap(rect, itemBounds)
                new_rects = self._clip_overlap(rect, overlap)
                result += new_rects
            else:
                result.append(rect)
        self.freerects = result
        self._remove_redundent()

    
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> None:
        pass


    def _find_best_score(self, item: Item):
        rects = []
        for rect in self.freerects:
            if self._item_fits_rect(item, rect):
                rects.append((self._score(rect, item), rect, False))
            if self._item_fits_rect(item, rect, rotation=True):
                rects.append((self._score(rect, item), rect, True))
        try:
            _score, rect, rot = min(rects, key=lambda x: x[0])
            return _score, rect, rot
        except ValueError:
            return None, None, False


    def insert(self, item: Item, heuristic: str = 'best_area') -> bool:
        """
        Public method for selecting heuristic and inserting item
        """
        _, best_rect, rotated = self._find_best_score(item)

        if best_rect:
            if rotated:
                item.rotate()
            item.x, item.y = best_rect.x, best_rect.y
            self.items.append(item)
            self.free_area -= item.area
            maximals = self._split_rectangle(best_rect, item)
            self.freerects.remove(best_rect)
            self.freerects += maximals
            itemBounds = self._item_bounds(item)

            self._prune_overlaps(itemBounds)
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


class MaxRectsBAF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return rect.area-item.area
        

class MaxRectsBSSF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return min(rect.width-item.width, rect.height-item.height)


class MaxRectsBLSF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return max(rect.width-item.width, rect.height-item.height)


class MaxRectsWAF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return 0 - (rect.area-item.area)
        

class MaxRectsWSSF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return 0 - min(rect.width-item.width, rect.height-item.height)


class MaxRectsWLSF(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return 0 - max(rect.width-item.width, rect.height-item.height)


class MaxRectsBL(MaximalRectangle):
    @staticmethod
    def _score(rect: FreeRectangle, item: Item) -> int:
        return rect.y + rect.height + item.height


class MaxRectsCP(MaximalRectangle):
    @staticmethod
    def _common_interval_length(Xstart: int, Xend: int,
                               Ystart: int, Yend: int) -> int:
        """
        Returns the length of perimiter shared by two
        rectangles
        """
        if Xend < Ystart or Yend < Xstart:
            return 0
        return min(Xend, Yend) - max(Xstart, Ystart)


    def _score(self, rect: FreeRectangle, item: Item) -> int:
        perim = 0
        if rect.x == 0 or rect.x + item.width == self.x:
            perim += item.height
        if rect.y == 0 or rect.y + item.height == self.y:
            perim += item.width

        for itm in self.items:
            if (itm.x == rect.x+rect.width or
                itm.x+itm.width == rect.x):
                perim += self._common_interval_length(itm.y, itm.y+itm.height, rect.y, rect.y+item.height)
            if (itm.y == rect.y+rect.height or
                item.y+itm.height == rect.y):
                perim += self._common_interval_length(itm.x, itm.x+itm.width, rect.x, rect.x+item.width)
        return 0 - perim
