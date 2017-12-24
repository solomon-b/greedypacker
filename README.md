# Two Dimensional Bin Packing
[![Build Status](https://travis-ci.org/ssbothwell/greedypacker.svg?branch=master)](https://travis-ci.org/ssbothwell/greedypacker)
[![Coverage Status](https://coveralls.io/repos/github/ssbothwell/greedypacker/badge.svg?branch=master)](https://coveralls.io/github/ssbothwell/greedypacker?branch=master)

Solomon Bothwell

ssbothwell@gmail.com

![Maximal Rectangle Rendering](https://raw.githubusercontent.com/ssbothwell/greedypacker/master/static/maximal_rectangleAlgorithm-bottom_leftHeuristic.png)

A 2D bin packing library based on on Jukka Jylänki's article ["A Thousand
Ways to Pack the Bin - A Practical Approach to Two-Dimensional Rectangle Bin
Packing."](http://clb.demon.fi/files/RectangleBinPack.pdf)

This library is intended for offline packing. All algorithms
heuristics and optimizations from Jukka's article are included.

A web demo made with Flask and ReactJS is available ["here"](https://ssbothwell.github.io/greedypacker-react/)
Packing performance varies drastically with different combinations of optimizations and
datasets, so its important to under the settings and test a variety of them.


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

#### Algorithms

##### ["Shelf"](https://github.com/ssbothwell/greedypacker/blob/master/docs/shelf.md)
##### ["Guillotine"](https://github.com/ssbothwell/greedypacker/blob/master/docs/guillotine.md)
##### ["Maximal Rectangles"](https://github.com/ssbothwell/greedypacker/blob/master/docs/maximal_rectangles.md)
##### ["Skyline"](https://github.com/ssbothwell/greedypacker/blob/master/docs/skyline.md)


#### General Optional Parameters:

All optimizations are passed in as keyword arguments when the GreedyPacker
instance is created:

##### Item Rotation
Item rotation can be disabled with the keyword argument `rotation=False`

##### Item Pre-Sort
Items can be pre-sorted according to a number of settings for 
the 'sorting_heuristic' keyword argument:

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
* False: Pack in the order added to the binmanager

##### Algorithm Specific optmizations/settings:
See the algorithm specific pages linked above.

### install notes

Requires Python`>=3.0`. 

### tests

```shell
python -m unittest test
```
