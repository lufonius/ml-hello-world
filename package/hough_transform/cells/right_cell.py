from .edge_cell import EdgeCell
from .cell import Cell
from .position import Position


class RightCell(EdgeCell):
    position = Position.RIGHT

    def __init__(self, parent: Cell):
        super().__init__(parent)

    def grow_leafes(self):
        self.children = [
            RightCell(self)
        ]