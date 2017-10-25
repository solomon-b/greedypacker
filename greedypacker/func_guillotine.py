#!/usr/bin/env python
"""
Functional Version of the Guillotine Algorithm

Solomon Bothwell
ssbothwell@gmail.com

"""
import typing
from typing import List, Iterator
from itertools import chain
from functools import partial, reduce
import item
#from . import guillotine

#FreeRectangle = guillotine.FreeRectangle

class FreeRectangle(typing.NamedTuple('FreeRectangle', [('width', int), ('height', int), ('x', int), ('y', int)])):
    __slots__ = ()
    @property
    def area(self):
        return self.width*self.height


def pass_state(func):
    def inner(args):
        return func(args), args
    return inner
    

def compose(*functions):
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def checkFit(freeRect: FreeRectangle, item: item.Item) -> bool:
    """ Returns true if the item fits the freeRect """
    Iw, Ih = item.width, item.height
    Fw, Fh = freeRect.width, freeRect.height
    
    return (Iw <= Fw and Ih <= Fh) or (Ih <= Fw and Iw <= Fh)


def filterFit(freeRects: List[FreeRectangle],
              item: item.Item) -> (List[FreeRectangle], item):
    checkFit_p = partial(checkFit, item=item)

    return filter(checkFit_p, freeRects)


def smallestWidth(freeRects: List[FreeRectangle]) -> List[FreeRectangle]:
    """ Returns the FreeRectangle with the smallest width """
    smallest = lambda F1, F2: F1 if (F1.width < F2.width) else F2
    return reduce(smallest, freeRects)


def validateRect(F: FreeRectangle) -> bool:
    """ return true if the rectangle is not degenerate """
    return False if ((F.width <= 0) or (F.height <= 0)) else True


def splitRect(F: FreeRectangle, I: item.Item, split: bool=True) -> Iterator[FreeRectangle]:
    """
    Given an Item and a split axis, return two FreeRectangles representing the remainder
    """
    top_x = F.x
    top_y = F.y + I.height
    top_h = F.height - I.height

    right_x = F.x + I.width
    right_y = F.y
    right_w = F.width - I.width
    
    # horizontal split
    if split:
        top_w = F.width
        right_h = I.height
    # vertical split
    else:
        top_w = I.width
        right_h = F.height

    right_rect = FreeRectangle(right_w, right_h, right_x, right_y)
    top_rect = FreeRectangle(top_w, top_h, top_x, top_y)

    return filter(validateRect, [right_rect, top_rect])
    

def splitRule(freeRect: FreeRectangle, item: item.Item, rule: str='default') -> bool:
    """
    Decides the split axis. Returns True for horizontal
    split and False for vertical split.
    """
    # Leftover lengths
    w = freeRect.width - item.width
    h = freeRect.height - item.height

    if rule == 'SplitShorterLeftoverAxis': split = (w <= h)
    elif rule == 'SplitLongerLeftoverAxis': split = (w > h)
    elif rule == 'SplitMinimizeArea': split = (item.width * h > w * item.height)
    elif rule == 'SplitMaximizeArea': split = (item.width * h <= w * item.height)
    elif rule == 'SplitShorterAxis': split = (freeRect.width <= freeRect.height)
    elif rule == 'SplitLongerAxis': split = (freeRect.width > freeRect.height)
    else: split = True

    return split


def removeRect(rect: FreeRectangle,
               freeRects: List[FreeRectangle]) -> List[FreeRectangle]:
    """ Filters a FreeRectangle from the list """
    return filter(lambda x: x != rect, freeRects)


def guillotine(freeRects: List[FreeRectangle],
               item: item.Item,
               split_rule: str='SplitLongerLeftoverAxis') -> list:
    """ 
    Wrapper Function

    Give a list of FreeRectangles and an Item,
    return the best fit FreeRectangle
    """
    checkFit_p = partial(checkFit, item=item)
    filter_p = partial(filter, checkFit_p)

    splitRule_p = partial(splitRule, item=item, rule=split_rule)
    split_p = partial(splitRect, I=item)
    split_wrapper = lambda F: split_p(F, split=splitRule_p(F))

    best_width = compose(smallestWidth, filter_p)
    #best_width = compose(list, split_wrapper, smallestWidth, filter_p)

    removeRect_p = partial(removeRect, freeRects=freeRects)

    return list(removeRect_p(best_width(freeRects)))


if __name__ == "__main__":
    F0 = FreeRectangle(5,4,0,0)
    F1 = FreeRectangle(2,2,0,0)
    F2 = FreeRectangle(4,4,0,0)
    I0 = item.Item(2,3)
    print(guillotine([F0, F1, F2], I0))
