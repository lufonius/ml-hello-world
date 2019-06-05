from package.hough_transform.cells.right_cell import RightCell
from .edge_cell import EdgeCell
from .cell import Cell
from .bottom_cell import BottomCell
from .position import Position


class BottomRightCell(EdgeCell):
    position = Position.BOTTOM_RIGHT

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            RightCell(self),
            BottomRightCell(self),
            BottomCell(self)
        ]