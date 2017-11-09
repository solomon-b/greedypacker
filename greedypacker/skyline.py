#!/usr/bin/env python
"""
Skyline 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
from typing import List, NamedTuple
from sortedcontainers import SortedList
from .item import Item


class SkylineSegment(NamedTuple):
    x: int
    y: int
    width: int


class Skyline:
    def __init__(self, width: int = 8,
                 height: int = 4,
                 rotation: bool = True) -> None:
        self.width = width
        self.height = height
        starting_segment = SkylineSegment(0, 0, width, 0)
        self.skyline = SortedList(starting_segment)
        self.items = [] # type: List[Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Skyline(%r)" % (self.items)


    @staticmethod
    def split_skyline(segment: SkylineSegment, item: Item) -> List[SkylineSegment]:
        """
        Removes the portion of a SkylineSegment on the bottom
        edge of an Item and returns segments for the top of the
        Item and the remainder to the right of the item.
        """
        new_segments = []
        if item.width <= segment.width:
            top_y = segment.y + item.height
            if top_y < self.height:
                top_segment = SkylineSegment(segment.x, top_y, item.width)
                new_segments.append(top_segment)
            right_x = segment.x + item.width
            if right_x < segment.x + segment.width:
                right_segment = SkylineSegment(right_x, segment.y, segment.width-item.width)
                new_segments.append(top_segment)
        return new_segments


    def merge_segments(self) -> None:
        """
        Merge any adjacent SkylineSegments
        """
        new_segments = SortedList()
        for i, segment in enumerate(self.skyline[:-1]):
            next_seg = self.skyline[i+1]
            if (segment.x + segment.width  == next_seg.x and
                segment.y == next_seg.y):
                new_seg = SkylineSegment(segment.x, segment.y, next_seg.width+segment.width)
                new_segments.append(new_seg)         
            else:
                new_segments.append(segment)
        self.skyline = new_segments


    def check_fit(self, item: Item, sky_index: int) -> bool:
        """
        Returns true if the item will fit about the skyline
        segment sky_index. Also works if the item is wider 
        then the segment.
        """
        x = self.skyline[i].x
        y = self.skyline[i].y
        i = sky_index
        width =  item.width

        if x + item.width > self.width:
            return False
        if y + item.height > self.height:
            return False

        while width > 0:
            y = max(y, self.skyline[i])
            if (y + item.height > self.height):
                return False
            width -= skyline[i].width
            i += 1
            if width > 0 and i == len(self.skyline):
                return False
        return True
            

    def bottom_left(self, item: Item) -> bool:
        """
        Inserts the item such that its top edge
        has the lowest available y coordinate.
        """

        best_height = float('inf')
        best_width = float('inf')
        best_seg = None
         
        for i, segment in enumerate(self.skyline):
            if self.check_fit(item, i):
                if item.height + segment.y < best_height:
                    best_seg = segment
                    best_height = item.height + segment.y
                    best_width = segment.width

        item.CornerPoint = (best_seg.x, best_seg.y)
        self.items.append(item)
        remainder_segments = self.split_skyline(best_seg, item)
        self.skyline.update(remainder_segments)
        self.skyline.remove(best_seg)
        self.merge_segments()
        return True


