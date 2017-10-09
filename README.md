# Two Dimensional Bin Packing
[![Build Status](https://travis-ci.org/ssbothwell/greedypacker.svg?branch=master)](https://travis-ci.org/ssbothwell/greedypacker)

Solomon Bothwell

ssbothwell@gmail.com

A 2D greedypackering library based on on Jukka Jylänki's article 
"A Thousand Ways to Pack the Bin - A Practical Approach to 
Two-Dimensional Rectangle Bin Packing."

This library is intended for offline greedypackering and takes
a greedy heuristic. Next Fit, First Fit, Best Width, Best
Height, Best Area, Worst Width, Worst Width, and Worst Area
heuristics are available for both Shelf and Guillotine style
cuts. 

The project is still in early development. Multi Bin ranking
and Maximal Rectangle Cut and Skyline Cuts will be included
along with the Waste Map and Rectangle Merge improvements.
See TODO.md for complete list of in progress features. 


### Example Usage:
```
In [13]: import greedypacker

In [14]: M = greedypacker.BinManager(8, 4)

In [15]: M.set_algorthim('shelf', 'best_width_fit')
Out[15]: True

In [16]: ITEM = greedypacker.Item(4, 2)

In [17]: ITEM2 = greedypacker.Item(5, 2)

In [18]: ITEM3 = greedypacker.Item(2, 2)

In [19]: M.add_items(ITEM, ITEM2, ITEM3)

In [20]: M.execute()

In [21]: M.items
Out[21]:
[Item(x=5, y=2, CornerPoint=(0, 0)),
 Item(x=4, y=2, CornerPoint=(0, 2)),
 Item(x=2, y=2, CornerPoint=(5, 0))]

```

Algorithm Choices:
* Shelf:
  Split the bin into rows based on the height of the first
  item in the row.

* Guillotine:
  Make orthogonal cuts into the bin to create areas that 
  match the sizes of the items.

Heuristic choices are:
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
    

### install notes

Requires Python`>=3.6` (for `typing.NamedTuple` usage).

### tests

```shell
python -m unittest test
```
