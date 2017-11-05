"""
2D Item class.
"""
class Item:
    """
    Items class for rectangles inserted into sheets
    """
    def __init__(self, width, height,
                 CornerPoint: tuple = (0, 0),
                 rotation: bool = True) -> None:
        self.width = width
        self.height = height
        self.CornerPoint = CornerPoint
        self.x = CornerPoint[0]
        self.y = CornerPoint[1]
        self.area = self.width * self.height
        self.rotated = False


    def __repr__(self):
        return 'Item(x=%r, y=%r, CornerPoint=%r)' % (self.width, self.height, self.CornerPoint)


    def rotate(self) -> None:
        self.width, self.height = self.height, self.width
        self.rotated = False if self.rotated == True else True


    def __lt__(self, other: 'Item') -> bool:
        return True if self.y < other.y else False


    def __le__(self, other: 'Item') -> bool:
        return True if self.y <= other.y else False


    def __gt__(self, other: 'Item') -> bool:
        return True if self.y > other.y else False


    def __ge__(self, other: 'Item') -> bool:
        return True if self.y >= other.y else False


