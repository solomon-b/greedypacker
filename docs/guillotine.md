### Guillotine Algorithm

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
#### Heuristic Choices
* best_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is smallest. Ties are broken with 
  `best_long`.
* best_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is smallest. Ties are broken with
  `best_shortside`.
* best_area:
  Choose the FreeRectangle with the smallest area that still fits
  the Item. Ties are broken with `best_shortside`.
* worst_shortside:
  Choose a FreeRectangle (F) where the shorter remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where min(Fw - Iw, Fh - Ih) is largest. Ties are broken with 
  `worst_long_side`.
* worst_longside:
  Choose a FreeRectangle (F) where the longer remainder side after
  inserted the Item (I) is minimized. ie, choose the FreeRectangle
  where max(Fw - Iw, Fh - Ih) is largest. Ties are broken with
  `worst_shortside`.
* worst_area:
  Choose the FreeRectangle with the largest area that still fits
  the Item. Ties are broken with `worst_shortside`.

#### Optional Optimizations:

All optimizations are passed in as keyword arguments when the GreedyPacker
instance is created:

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
