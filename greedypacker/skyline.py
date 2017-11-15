#!/usr/bin/env python
"""
Skyline 2D Bin Algorithm

Solomon Bothwell
ssbothwell@gmail.com
"""
import operator
import typing
from typing import List, NamedTuple, Tuple
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
        starting_segment = SkylineSegment(0, 0, width)
        self.skyline = SortedList([starting_segment])
        self.items = [] # type: List[Item]
        self.rotation = rotation


    def __repr__(self) -> str:
        return "Skyline(%r)" % (self.items)


    @staticmethod
    def clip_segment(segment: SkylineSegment, item: Item) -> List[SkylineSegment]:
        """
        Clip out the length of segment adjacent to the item. 
        Return the rest.
        """
        # Segment not under new item
        item_end_x = item.CornerPoint[0] + item.width
        if segment.x > item.x+item.width:
            return [segment]
        # Segment fully under new item
        elif segment.x >= item.CornerPoint[0] and segment.width+segment.x <= item_end_x:
            return []
        # Segment partialy under new item (to the left)
        elif segment.x < item.CornerPoint[0] and segment.x+segment.width <= item_end_x:
            new_segment = SkylineSegment(segment.x, segment.y, item.CornerPoint[0]-segment.x)        
            return [new_segment]
        # Segment partially under new item (to the right)
        elif segment.x >= item.CornerPoint[0] and segment.x+segment.width > item_end_x:
            new_segment = SkylineSegment(item_end_x, segment.y, (segment.x+segment.width)-item_end_x)
            return [new_segment]
        # Segment wider then item in both directions
        elif segment.x < item.CornerPoint[0] and segment.x+segment.width > item_end_x:
            new_segment_left = SkylineSegment(segment.x, segment.y, item.CornerPoint[0]-segment.x)
            new_segment_right = SkylineSegment(item_end_x, segment.y, (segment.x+segment.width)-item_end_x)
            return [new_segment_left, new_segment_right]
        else:
            return []


    def update_segment(self, segment: SkylineSegment, item: Item) -> List[SkylineSegment]:
        """
        Clips the line segment under the new item and returns
        an updated skyline segment list.
        """
        new_segments = SortedList([])
        for seg in self.skyline:
            new_segments.update(self.clip_segment(seg, item))

        # Create new segment if room above item
        if item.height + item.CornerPoint[1] < self.height:
            new_seg_y = segment.y + item.height
            new_seg = SkylineSegment(segment.x, new_seg_y, item.width)
            new_segments.add(new_seg)
       
        return new_segments


    def merge_segments(self) -> None:
        """
        Merge any adjacent SkylineSegments
        """
        new_segments = SortedList([self.skyline[0]])
        for seg in self.skyline[1:]:
            last = new_segments[-1]
            if seg.y == last.y:
                if (seg.x >= last.x and 
                    seg.x <= last.x+last.width):
                    if seg.x+seg.width > last.x+last.width:
                        new_last = SkylineSegment(last.x, last.y, 
                                                  seg.x+seg.width)
                        new_segments.remove(last)
                        new_segments.add(new_last)
                        continue
            new_segments.add(seg)

        self.skyline = new_segments


    def check_fit(self, item: Item, sky_index: int) -> Tuple[bool, int]:
        """
        Returns true if the item will fit above the skyline
        segment sky_index. Also works if the item is wider 
        then the segment.
        """
        i = sky_index
        x = self.skyline[i].x
        y = self.skyline[i].y
        width = item.width

        if x + item.width > self.width:
            return (False, None)
        if y + item.height > self.height:
            return (False, None)

        while width > 0:
            y = max(y, self.skyline[i].y)
            if (y + item.height > self.height):
                return (False, None)
            width -= self.skyline[i].width
            i += 1
            if width > 0 and i == len(self.skyline):
                return (False, None)
        return (True, y)
            

    def bottom_left(self, item: Item) -> bool:
        """
        Inserts the item such that its top edge
        has the lowest available y coordinate.
        """

        best_height = float('inf')
        best_width = float('inf')
        best_seg = None
        best_y = None
        rotation = False
         
        for i, segment in enumerate(self.skyline):
            fits, y = self.check_fit(item, i)
            if fits:
                if ((item.height+segment.y < best_height) or 
                    (segment.y+item.height == best_height and
                    segment.width < best_width)):
                    best_seg = segment
                    best_height = item.height + y
                    best_width = segment.width
                    best_y = y
                if ((item.width+segment.y < best_height) or
                    (segment.y+item.width == best_height and
                    segment.width < best_width)):
                    rotation = True
                    best_seg = segment
                    best_height = item.width + y
                    best_width = segment.width
                    best_y = y
        if best_seg:
            if rotation:
                item.rotate()
            item.CornerPoint = (best_seg.x, best_y)
            self.items.append(item)
            self.skyline = self.update_segment(best_seg, item)
            self.merge_segments()
            return True
        return False


