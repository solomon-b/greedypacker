# Two Dimensional Bin Packing
Solomon Bothwell

ssbothwell@gmail.com


A library for two dimensional bin packing using a greedy approach.

Items are tuples of width, height values. A list of Items
are submitted, sorted, and placed in bins according to the chosen
heuristic. Layouts are returned as nested lists of namedtuples.
Each item is returned with its dimensions, xy position (top left 
corner referenced), and bin ID. 

### Example Usage:
```
>>> BINSET = binpack.BinPack()
>>> BINSET.insert((2, 4), (2, 2), (4, 5), (4, 4), (2, 2), (3, 2), heuristic='best_fit')
>>> BINSET.print_layouts()
{'width': 4, 'height': 8, 'area': 32, 'efficiency': 0.8125, 'items': [(CornerPoint(x=0, y=0), Item(width=4, height=5)), (CornerPoint(x=0, y=5), Item(width=3, height=2))]}
{'width': 4, 'height': 8, 'area': 32, 'efficiency': 1.0, 'items': [(CornerPoint(x=0, y=0), Item(width=4, height=4)), (CornerPoint(x=0, y=4), Item(width=2, height=4)), (CornerPoint(x=2, y=4), Item(width=2, height=2)), (CornerPoint(x=2, y=6), Item(width=2, height=2))]}
```

Heuristic choices are:
*next_fit:
    When processing the next item, see if it fits in the same bin
    as the last item. Start a new bin only if it does not.
*best_fit:
    When processing the next item, place it in the bin that results
    in the smallest remaining space. Start a new bin if it fits no
    bins.
    
Items are automatically sorted by area in descending order. Sorting 
can be disabled by using setting the named argument `sorting=False`
when you instantiate the binset. This can be desirable for online packing
applications.
