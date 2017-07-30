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
>>> BINSET = BinPack(bin_dims=(4,8))
>>> BINSET.insert((2, 4), (2, 2), (4, 5), (4, 4), (2, 2), (3, 2), heuristic='best_fit')
>>> BINSET.print_layouts()
```

