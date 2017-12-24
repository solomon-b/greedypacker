### Skyline Algorithm

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

#### Heuristics
* bottom_left:
  see Maximal Rectangle bottom_left above.
* best_fit:
  place the item such that the amount of space lost to wastemap
  is minimized. Ties are broken with `bottom_left`.

#### Optional Optimizations:

All optimizations are passed in as keyword arguments when the GreedyPacker
instance is created:

###### Wastemap
The skyline algorithm can potentially lose track of empty space caught behind the
skyline. This space can be recovered using a wastemap like in the shelf algorithm.
It is highly recommended that this is enabled when using the skyline algorithm and
is set True by default. 

Usage:
```
In [15]: M = greedypacker.BinManager(8, 4, 'shelf', 'best_width_fit', wastemap=True)
```
