# Two Dimensional Bin Packing
[![Build Status](https://travis-ci.org/ssbothwell/greedypacker.svg?branch=master)](https://travis-ci.org/ssbothwell/greedypacker)
[![Coverage Status](https://coveralls.io/repos/github/ssbothwell/greedypacker/badge.svg?branch=master)](https://coveralls.io/github/ssbothwell/greedypacker?branch=master)

Solomon Bothwell

ssbothwell@gmail.com

A 2D bin packing library based on on Jukka Jylänki's article ["A Thousand
Ways to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin
Packing."](http://clb.demon.fi/files/RectangleBinPack.pdf)

This library is intended for offline packing. All algorithms
heuristics and optimizations from Jukka's article are included.


### Example Usage:
```
In [1]: import greedypacker

In [2]: M = greedypacker.BinManager(8, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=True, rotation=True)

In [3]: ITEM = greedypacker.Item(4, 2)

In [4]: ITEM2 = greedypacker.Item(5, 2)

In [5]: ITEM3 = greedypacker.Item(2, 2)

In [6]: M.add_items(ITEM, ITEM2, ITEM3)

In [7]: M.execute()

In [8]: M.bins
Out[8]: [Sheet(width=8, height=4, shelves=[{'y': 2, 'x': 8, 'available_width': 0, 'area': 6, 'vertical_offset': 0, 'items': [Item(width=5, height=2, x=0, y=0)]}, {'y': 2, 'x': 8, 'available_width': 4, 'area': 8, 'vertical_offset': 2, 'items': [Item(width=4, height=2, x=0, y=2)]}])]
```

#### Algorithm Choices:
* Shelf:

  ![Shelf Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/shelfAlgorithm-next_fitHeuristic.png)

  Divide the bin into horizontal rows with heights equal to the
  first Item inserted. Track the rows in a list and choose a
  row using whichever desired heuristic.

  Sample Code:
  ```
  M = greedypacker.BinManager(8, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=True, rotation=True)
  ```

* Guillotine:

  ![Guillotine Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/guillotineAlgorithm-best_shortsideHeuristic.png)

  Place items into the bin starting with its lower left corner.
  For each insertion, split the bin into smaller sections
  (FreeRectangles) which are tracked in a list. Whenever a new
  item is inserted into the bin, find a FreeRectangle using
  whichever heuristic then place the item into that FreeRectangle's
  lower left corner. If there is left over width or height in
  the FreeRectangle, split the FreeRectangle so that the remainder
  space makes up its own FreeRectangle(s).

  Sample Code:
  ```
  M = greedypacker.BinManager(8, 4, pack_algo='guillotine', heuristic='best_longside', rectangle_merge=True, rotation=True)
  ```

* Maximal Rectangles:

  ![Maximal Rectangle Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/maximal_rectangleAlgorithm-bottom_leftHeuristic.png)

  Rather then choosing a split axis like in the Guillotine Algorithm, Maximal
  Rectangles adds both possible splits to the list of FreeRectangles. This
  ensures that the largest possible rectangular areas are present in the
  FreeRectangles list at all times.  

  Because a single point in the bin can now be represented by multiple
  FreeRectangles, the list must be carefully pruned between Item insertions.
  Any FreeRectangle that intersects the area occupied by the newly inserted
  Item is split such to remove the intersection. Additionally, any
  FreeRectangle which is fully overlapped by another FreeRectangle is deleleted
  from the list.

  ```
  M = greedypacker.BinManager(8, 4, pack_algo='maximal_rectangle', heuristic='bottom_left', rotation=True)
  ```

* Skyline:

  ![Skyline Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/skylineAlgorithm-bottom_leftHeuristic.png)

  Rather then track a list of all FreeRectangles or Shelves, the Skyline
  algorithm packs the list from bottom to top and only tracks the top edge of
  the topmost items packed into the bin.  This creates a 'skyline', or
  envelope. The skyline list grows linearly with the number of packed items.

  Because it only tracks the topmost edge, this algorithm is lossy and has the
  potential to lose track of useable space trapped behind the skyline. This can
  be countered by using the wastemap optimization from the Shelf algorithm.

  ```
  S = greedypacker.BinManager(8, 4, pack_algo='skyline', heuristic='bottom_left', rotation=True)
  ```

#### Shelf Heuristic choices:
* next_fit:
  Check the currently open Shelf and insert if the item fits.
  Otherwise create a new shelf and close the previous shelf.
* first_fit: 
  Loop through all the shelves or FreeRectangles and place the 
  item in the first one it fits.
* best_width_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the least remaining free width.
* best_height_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the least remaining free height.
* best_area_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the least remaining free area.
* worst_width_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the most remaining free width.
* worst_height_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the most remaining free height.
* worst_area_fit:
  Place the item in the shelf or FreeRectangle which would result
  in the most remaining free area.

#### Guillotine Heuristic Choices
* best_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is smallest.
* best_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is smallest.
* best_area:
  Choose the FreeRectangle with the smallest area that still fits
  the Item.
* worst_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is largest.
* worst_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is largest.
* worst_area:
  Choose the FreeRectangle with the largest area that still fits
  the Item.

#### Additional Maximal Rectangle Heuristic Choices
Maximal Rectangles uses all the Guillotine heuristics plus the
following:
* bottom_left:
  Choose the FreeRectangle where the Y coordinate of the Item's
  top side is smallest. If there is a tie, pick the choice with
  the smallest X coordinate.
* contact_point:
  Choose the FreeRectangle where the maximum amount of the Item's
  perimiter is touching either occupied space or the edges of
  the bin.

#### Skyline Heuristics
* bottom_left:
  see Maximal Rectangle bottom_left above.
* best_fit:
  place the item such that the amount of space lost to wastemap
  is minimized.

#### Optional Optimizations:

All optimizations are passed in as keyword arguments when the GreedyPacker
instance is created:

##### Item Pre-Sort
Items can be pre-sorted according to a number of settings for 
the 'sorting_heuristic' named argument:

* ASCA: Sort By Area Ascending
* DESCA: Sort By Area Descending (This is the default setting)
* ASCSS: Sort By Shorter Side Ascending
* DESCSS: Sort By Shorter Side Descending
* ASCLS: Sort By Longer Side Ascending
* DESCLS: Sort By Longer Side Descending
* ASCPERIM: Sort By Perimeter Ascending
* DESCPERIM: Sort By Perimeter Descending
* ASCDIFF: Sort by The ABS Difference Between Sides Ascending
* DESCDIFF: Sort By The ABS Difference Between Sides Descending
* ASCRATIO: Sort By The Ratio of The Sides Ascending
* DESCRATIO: Sort By The Ratio of The Sides Descending

Sorting can be disabled by setting the 'sorting' named argument to False.

##### Shelf Packing:

###### Wastemap
Shelf packing items of disparate heights results in a lot of wasted space
above each item on a shelf. This optimization uses the Guillotine algorithm
to track that wasted area and attempts to insert Items into it. The
wastemap is updated each time an Item is unable to fit the existing shelves
and before a new shelf is created.  

Usage:
```
In [15]: M = greedypacker.BinManager(8, 4, 'shelf', 'best_width_fit', wastemap=True)
```

##### Guillotine Packing:

###### Rectangle Merge
The guillotine algorithm has a tendency to leave fragmented
groupings of FreeRectangles which could potentially be connected
into larger FreeRectangles. This optimization Defragments the 
FreeRectangle list between each item insertion.

Usage:
```
In [15]: M = greedypacker.BinManager(8, 4, 'guillotine', 'best_width_fit', rectangle_merge=True)
```

###### Split Rules
In a guillotine cut we have the choice of splitting along the horizontal or
the vertical axis. By default Greedypacker will split along the horizontal
axis. However, Jukka specifies 6 different splitting rules which can result
in more efficient packings then the default always horizontal split.

* 'SplitShorterLeftoverAxis' - split on the horizontal axis if the leftover width of the freerectnage (freerectangle.width - item.width) is less then the leftover height.
* 'SplitLongerLeftoverAxis' - split on the horizontal axis if the leftover width of the freerectnage (freerectangle.width - item.width) is greater then the leftover height.
* 'SplitShorterAxis' - Split on the horizontal axis if FreeRectangle.width <= FreeRectangle.height. Otherwise split on the vertical axis.
* 'SplitLongerAxis' - Split on the horizontal axis if FreeRectangle.width >= FreeRectangle.height. Otherwise split on the vertical axis.
* 'SplitMinimizeArea' - Count the area of the quadrant above the Item (A0) and to the right of the item (A1). Split the rectangle so that the space above and to the right of the Item (A3) is connected to the smaller quadrant.
* 'SplitMaximizeArea' - The same as SplitMinimizeArea but A3 is connected to the larger quadrant.

Usage:
```
In [15]: M = greedypacker.BinManager(8, 4, 'guillotine', 'best_width_fit', split_heuristic='SplitMinimizeArea')
```

##### Shelf Packing:

###### Wastemap
See the Shelf wastemap description above.

### install notes

Requires Python`>=3.0`. 

### tests

```shell
python -m unittest test
```
