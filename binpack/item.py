"""
2D Item class.
"""
class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, x, y,
                 CornerPoint: tuple = (0, 0),
                 rotation: bool = True) -> None:
        if rotation:
            self.x = x if x > y else y
            self.y = y if y < x else x
        else:
            self.x = x
            self.y = y
        self.CornerPoint = CornerPoint


    def __repr__(self):
        return 'Item(x=%r, y=%r, CornerPoint=%r)' % (self.x, self.y, self.CornerPoint)


    def rotate(self) -> None:
        self.x, self.y = self.y, self.x


    def area(self) -> int:
        return self.x * self.y
    def __lt__(self, other: 'Item') -> bool:
        return True if self.y < other.y else False


    def __le__(self, other: 'Item') -> bool:
        return True if self.y <= other.y else False


    def __gt__(self, other: 'Item') -> bool:
        return True if self.y > other.y else False


    def __ge__(self, other: 'Item') -> bool:
        return True if self.y >= other.y else False


