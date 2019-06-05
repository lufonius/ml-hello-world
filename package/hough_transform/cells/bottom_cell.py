from package.hough_transform.cells.cell import Cell
from .edge_cell import EdgeCell
from .position import Position


class BottomCell(EdgeCell):
    position = Position.BOTTOM

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            BottomCell(self)
        ]
