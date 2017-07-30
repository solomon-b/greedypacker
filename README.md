# Two Dimensional Bin Packing
Solomon Bothwell
ssbothwell@gmail.com


A library for two dimensional bin packing using a greedy approach.

Items are tuples of width, height values. A list of Items
are submitted, sorted, and placed in bins according to the chosen
heuristic. Layouts are returned as nested lists of namedtuples.
Each item is returned with its dimensions, xy position (top left 
corner referenced), and bin ID. 

## Example Usage:

### Instantiate a bin set. Mode selects heuristic, first fit is default
BINSET = BinPack(bin_dims=(4,8))

#### Add items to the binset
#### Any number of items can be inserted as *args, heuristic choices are
#### currently next_fit and best_fit. Items are automatically sorted in 
#### decreasing order by item area.
BINSET.insert((2, 4), (2, 2), (4, 5), (4, 4), (2, 2), (3, 2), heuristic='best_fit')

#### Return Bin Layouts
BINSET.print_layouts()
