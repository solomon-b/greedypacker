# Two Dimensional Bin Packing
[![Build Status](https://travis-ci.org/ssbothwell/greedypacker.svg?branch=master)](https://travis-ci.org/ssbothwell/greedypacker)

Solomon Bothwell

ssbothwell@gmail.com

A 2D greedypackering library based on on Jukka Jylänki's article ["A Thousand
Ways to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin
Packing."](http://clb.demon.fi/files/RectangleBinPack.pdf)

This library is intended for offline greedypackering and takes a greedy
heuristic. Next Fit, First Fit, Best Width, Best Height, Best Area, Worst
Width, Worst Width, and Worst Area heuristics are available for both Shelf and
Guillotine style cuts.  

The project is still in early development. Maximal Rectangle Cut and Skyline
Cuts will be included along with the full set of opimitizations outlined in
Jukka's article.  See TODO.md for complete list of in progress features.  

### Example Usage:
```

In [7]: import greedypacker

In [8]: M = greedypacker.BinManager(8,4, pack_algo='s
   ...: helf', heuristic='best_width_fit', wastemap=T
   ...: rue, rotation=True)

In [9]: ITEM = greedypacker.Item(4, 2)

In [10]: ITEM2 = greedypacker.Item(5, 2)

In [11]: ITEM3 = greedypacker.Item(2, 2)

In [12]: M.add_items(ITEM, ITEM2, ITEM3)

In [13]: M.execute()

In [14]: M.bins
Out[14]: [Sheet(width=8, height=4, shelves=[{'y': 2, 'x': 8, 'available_width': 0, 'vertical_offset': 0, 'items': [Item(x=5, y=2, CornerPoint=(0, 0))]}, {'y': 2, 'x': 8, 'available_width': 4, 'vertical_offset': 2, 'items': [Item(x=4, y=2, CornerPoint=(0, 2))]}])]
```

#### Algorithm Choices:
* Shelf:
  Split the bin into rows based on the height of the first
  item in the row.

* Guillotine:
  Make orthogonal cuts into the bin to create areas that 
  match the sizes of the items.

#### Heuristic choices:
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

#### Optional Optimizations:

All optimizations are passed in as keyword arguments when the GreedyPacker
instance is created:

    
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
Defragments the Free Rectangles between each item insertion.

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

### install notes

Requires Python`>=3.0`. 

### tests

```shell
python -m unittest test
```
