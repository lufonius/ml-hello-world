from .bottom_cell import BottomCell
from .edge_cell import EdgeCell
from .cell import Cell
from .left_cell import LeftCell
from .position import Position

class BottomLeftCell(EdgeCell):
    position = Position.BOTTOM_LEFT

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            LeftCell(self),
            BottomLeftCell(self),
            BottomCell(self)
        ]