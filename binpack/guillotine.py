#!/usr/bin/env python
"""
Guillotine Style 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
from collections import namedtuple
from item import Item


FreeRectangle = namedtuple('FreeRectangle', ['width', 'height', 'x', 'y'])


class Guillotine:
    def __init__(self, x: int = 8, y: int = 4) -> None:
        self.x = x
        self.y = y
        self.freerects = [FreeRectangle(self.x, self.y, 0, 0)] # type: List[tuple]
        self.items = [] # type: List[Item]


    def __repr__(self) -> None:
        return "Guillotine(%r)" % (self.items)


    def first_fit(self, item: Item) -> bool:
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                item.CornerPoint = (freerect.x, freerect.y)
                self.items.append(item)
                self.freerects.remove(freerect)
                if item.x < freerect.width:
                    # generate free rectangle for remaining width
                    right_width = freerect.width - item.x
                    right_height = item.y
                    right_x = freerect.x + item.x
                    right_y = freerect.y
                    right_rect = FreeRectangle(right_width,
                                               right_height,
                                               right_x,
                                               right_y)
                    self.freerects.append(right_rect)
                if item.y < freerect.height:
                    top_width = freerect.width
                    top_height = freerect.height - item.y
                    top_x = freerect.x
                    top_y = item.y
                    top_rect = FreeRectangle(top_width,
                                             top_height,
                                             top_x,
                                             top_y)
                    self.freerects.append(top_rect)
                return True
        return False


    def best_width_fit(self, item) -> bool:
        best = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                elif freerect.width < best.width:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def best_height_fit(self, item) -> bool:
        best = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                elif freerect.height < best.height:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def best_area_fit(self, item) -> bool:
        best = None
        best_area = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                    best_area = best.width * best.height
                elif (freerect.height * freerect.width) < best_area:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def worst_width_fit(self, item) -> bool:
        best = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                elif freerect.width > best.width:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def worst_height_fit(self, item) -> bool:
        best = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                elif freerect.height > best.height:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def worst_area_fit(self, item) -> bool:
        best = None
        best_area = None
        for freerect in self.freerects:
            if item.x <= freerect.width and item.y <= freerect.height:
                if not best:
                    best = freerect
                    best_area = best.width * best.height
                elif (freerect.height * freerect.width) > best_area:
                    best = freerect

        if best:
            item.CornerPoint = (freerect.x, freerect.y)
            self.items.append(item)
            self.freerects.remove(best)
            if item.x < freerect.width:
                # generate free rectangle for remaining width
                right_width = freerect.width - item.x
                right_height = item.y
                right_x = freerect.x + item.x
                right_y = freerect.y
                right_rect = FreeRectangle(right_width,
                                           right_height,
                                           right_x,
                                           right_y)
                self.freerects.append(right_rect)
            if item.y < freerect.height:
                top_width = freerect.width
                top_height = freerect.height - item.y
                top_x = freerect.x
                top_y = item.y
                top_rect = FreeRectangle(top_width,
                                         top_height,
                                         top_x,
                                         top_y)
                self.freerects.append(top_rect)
            print(best, item)
            return True
        return False


    def __insert__(self, item: Item) -> bool:
        pass


    def bin_stats(self) -> dict:
        """
        Returns a dictionary with compiled stats on the bin tree
        """

        stats = {
            'width': self.x,
            'height': self.y,
            'area': self.x * self.y,
            'efficiency': 1-(sum([F.width*F.height for F in self.freerects])/(self.x*self.y)),
            'items': self.items,
            }

        return stats

if __name__ == '__main__':
    G = Guillotine(8, 4)
    I = Item(2,5)
    I2 = Item(2,4)
    I3 = Item(2,2)
    G.best_width_fit(I)
    G.best_width_fit(I2)
    G.best_width_fit(I3)
    print(G.items)
    print(G.freerects)
    print(G.bin_stats())
