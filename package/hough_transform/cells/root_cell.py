from .cell import Cell
from .bottom_left_cell import BottomLeftCell
from .bottom_cell import BottomCell
from .bottom_right_cell import BottomRightCell
from .left_cell import LeftCell
from .top_left_cell import TopLeftCell
from .top_cell import TopCell
from .top_right_cell import TopRightCell
from .right_cell import RightCell


class RootCell(Cell):

    def __init__(self, x: int, y: int, value: int):
        super().__init__(x, y, value)

    def grow_leafes(self):
        self.children = [
            TopLeftCell(self),
            TopCell(self),
            TopRightCell(self),
            RightCell(self),
            BottomRightCell(self),
            BottomCell(self),
            BottomLeftCell(self),
            LeftCell(self)
        ]