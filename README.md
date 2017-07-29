# Two Dimensional Bin Packing
Solomon Bothwell
ssbothwell@gmail.com


A first fit greedy algorithm for two dimensional offline bin packing.

Items are tuples of width, height values. A list of Items
are submitted, sorted, and placed in bins according to the chosen
heuristic. Layouts are returned as nested lists, or as JSON data.
Each item is returned with its dimensions, xy position (top left 
corner referenced), and bin ID. 

# Example Usage:

# Instantiate a bin set. Mode selects heuristic, first fit is default
BIN_SET = BinPack(bin_dims=(4,8), mode='best')

# Add items to binset
# item = (width, height)
ITEMS = [(3,4), (4,5), (6,8), (5,5), (1,2), (1,2), (3,2)]
BIN_SET.add(ITEMS)

# Return Layout
# For JSON add 'json=True' kwarg
print(BIN_SET.layout())
