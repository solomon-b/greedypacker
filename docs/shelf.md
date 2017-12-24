### Shelf Algorithm
  ![Shelf Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/shelfAlgorithm-next_fitHeuristic.png)

  Divide the bin into horizontal rows with heights equal to the
  first Item inserted. Track the rows in a list and choose a
  row using whichever desired heuristic.

  Sample Code:
  ```
  M = greedypacker.BinManager(8, 4, pack_algo='shelf', heuristic='best_width_fit', wastemap=True, rotation=True)
  ```

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
